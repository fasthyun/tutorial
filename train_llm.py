#!/usr/bin/env python3
"""
LLM Model Training Script
=========================
A comprehensive training script for fine-tuning Large Language Models (LLMs)
using Hugging Face Transformers and PyTorch.

Features:
- Supports multiple model architectures (GPT-2, LLaMA, etc.)
- Custom dataset loading from text files or JSON
- Distributed training support
- Mixed precision training (FP16/BF16)
- Gradient checkpointing for memory efficiency
- Learning rate scheduling with warmup
- Checkpoint saving and resumption
- Comprehensive logging and metrics tracking

Usage:
    python train_llm.py --model_name gpt2 --data_path data.txt --output_dir ./output

Author: AI Assistant
"""

import os
import json
import argparse
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field

import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    get_scheduler,
)
from transformers.trainer_callback import TrainerCallback
import datasets
from datasets import load_dataset


@dataclass
class ModelArguments:
    """Arguments pertaining to which model/config/tokenizer we are going to fine-tune."""
    
    model_name_or_path: str = field(
        default="gpt2",
        metadata={"help": "Path to pretrained model or model identifier from huggingface.co/models"}
    )
    config_name: Optional[str] = field(
        default=None,
        metadata={"help": "Pretrained config name or path if not the same as model_name"}
    )
    tokenizer_name: Optional[str] = field(
        default=None,
        metadata={"help": "Pretrained tokenizer name or path if not the same as model_name"}
    )
    cache_dir: Optional[str] = field(
        default=None,
        metadata={"help": "Where to store the pretrained models downloaded from huggingface.co"}
    )
    use_fast_tokenizer: bool = field(
        default=True,
        metadata={"help": "Whether to use one of the fast tokenizer backends by the transformers library."}
    )
    model_revision: str = field(
        default="main",
        metadata={"help": "The specific model version to use (can be a branch name, tag name or commit id)."}
    )
    trust_remote_code: bool = field(
        default=False,
        metadata={"help": "Whether to trust remote code when loading models."}
    )


@dataclass
class DataArguments:
    """Arguments pertaining to what data we are going to input our model for training and eval."""
    
    data_path: str = field(
        metadata={"help": "Path to the training data (text file or JSON)."}
    )
    validation_split: float = field(
        default=0.1,
        metadata={"help": "Fraction of data to use for validation."}
    )
    max_seq_length: int = field(
        default=512,
        metadata={"help": "Maximum sequence length for input tokens."}
    )
    preprocessing_num_workers: int = field(
        default=4,
        metadata={"help": "Number of processes to use for preprocessing."}
    )
    overwrite_cache: bool = field(
        default=False,
        metadata={"help": "Overwrite the cached training and evaluation sets"}
    )


@dataclass
class TrainingArgs:
    """Custom training arguments."""
    
    output_dir: str = field(
        default="./output",
        metadata={"help": "The output directory where the model predictions and checkpoints will be written."}
    )
    num_train_epochs: int = field(
        default=3,
        metadata={"help": "Total number of training epochs to perform."}
    )
    per_device_train_batch_size: int = field(
        default=4,
        metadata={"help": "Batch size per GPU/TPU core/CPU for training."}
    )
    per_device_eval_batch_size: int = field(
        default=4,
        metadata={"help": "Batch size per GPU/TPU core/CPU for evaluation."}
    )
    gradient_accumulation_steps: int = field(
        default=1,
        metadata={"help": "Number of updates steps to accumulate before performing a backward/update pass."}
    )
    learning_rate: float = field(
        default=5e-5,
        metadata={"help": "The initial learning rate for AdamW optimizer."}
    )
    weight_decay: float = field(
        default=0.01,
        metadata={"help": "Weight decay for AdamW optimizer."}
    )
    warmup_ratio: float = field(
        default=0.1,
        metadata={"help": "Ratio of total training steps used for a linear warmup from 0 to learning_rate."}
    )
    lr_scheduler_type: str = field(
        default="cosine",
        metadata={"help": "The scheduler type to use."}
    )
    fp16: bool = field(
        default=False,
        metadata={"help": "Whether to use fp16 (mixed) precision instead of 32-bit."}
    )
    bf16: bool = field(
        default=False,
        metadata={"help": "Whether to use bf16 (mixed) precision instead of 32-bit."}
    )
    gradient_checkpointing: bool = field(
        default=False,
        metadata={"help": "If True, use gradient checkpointing to save memory at the expense of slower backward pass."}
    )
    save_steps: int = field(
        default=500,
        metadata={"help": "Save checkpoint every X updates steps."}
    )
    logging_steps: int = field(
        default=10,
        metadata={"help": "Log every X updates steps."}
    )
    seed: int = field(
        default=42,
        metadata={"help": "Random seed for reproducibility."}
    )


class TextDataset(Dataset):
    """Custom dataset for loading text data."""
    
    def __init__(self, data_path: str, tokenizer, max_length: int = 512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.examples = []
        
        # Load data based on file extension
        if data_path.endswith('.json'):
            self._load_json(data_path)
        elif data_path.endswith('.txt'):
            self._load_text(data_path)
        else:
            raise ValueError(f"Unsupported file format: {data_path}")
        
        print(f"Loaded {len(self.examples)} examples from {data_path}")
    
    def _load_text(self, data_path: str):
        """Load plain text file (one example per line or chunked)."""
        with open(data_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Split into chunks
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        
        # Create overlapping chunks
        stride = self.max_length // 2
        for i in range(0, len(tokens), stride):
            chunk = tokens[i:i + self.max_length]
            if len(chunk) > 0:
                self.examples.append(chunk)
    
    def _load_json(self, data_path: str):
        """Load JSON file with 'text' field."""
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and 'text' in item:
                    text = item['text']
                elif isinstance(item, str):
                    text = item
                else:
                    continue
                
                encoded = self.tokenizer.encode(text, add_special_tokens=False, truncation=True, max_length=self.max_length)
                if len(encoded) > 0:
                    self.examples.append(encoded)
        elif isinstance(data, dict) and 'texts' in data:
            for text in data['texts']:
                encoded = self.tokenizer.encode(text, add_special_tokens=False, truncation=True, max_length=self.max_length)
                if len(encoded) > 0:
                    self.examples.append(encoded)
    
    def __len__(self) -> int:
        return len(self.examples)
    
    def __getitem__(self, idx: int) -> Dict[str, torch.Tensor]:
        example = self.examples[idx]
        input_ids = torch.tensor(example, dtype=torch.long)
        
        # Create attention mask (all 1s since we don't have padding yet)
        attention_mask = torch.ones_like(input_ids)
        
        # Labels are the same as input_ids for causal language modeling
        labels = input_ids.clone()
        
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }


class LoggingCallback(TrainerCallback):
    """Custom callback for logging training metrics."""
    
    def on_log(self, args, state, control, logs=None, **kwargs):
        if logs is not None:
            print(f"\n[Step {state.global_step}]")
            for key, value in logs.items():
                if isinstance(value, (int, float)):
                    print(f"  {key}: {value:.4f}")


def load_and_preprocess_data(
    data_path: str,
    tokenizer,
    max_seq_length: int,
    validation_split: float = 0.1):
    """Load and preprocess the dataset."""
    
    dataset = TextDataset(data_path, tokenizer, max_seq_length)
    
    # Split into train and validation
    if validation_split > 0:
        split_idx = int(len(dataset) * (1 - validation_split))
        train_dataset = torch.utils.data.Subset(dataset, range(split_idx))
        eval_dataset = torch.utils.data.Subset(dataset, range(split_idx, len(dataset)))
        print(f"Train samples: {len(train_dataset)}, Validation samples: {len(eval_dataset)}")
    else:
        train_dataset = dataset
        eval_dataset = None
    
    return train_dataset, eval_dataset


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Train an LLM model')
    
    # Model arguments
    parser.add_argument('--model_name', type=str, default='gpt2',
                        help='Model name or path (default: gpt2)')
    parser.add_argument('--config_name', type=str, default=None,
                        help='Config name or path')
    parser.add_argument('--tokenizer_name', type=str, default=None,
                        help='Tokenizer name or path')
    parser.add_argument('--cache_dir', type=str, default=None,
                        help='Cache directory for models')
    parser.add_argument('--trust_remote_code', action='store_true',
                        help='Trust remote code for custom models')
    
    # Data arguments
    parser.add_argument('--data_path', type=str, required=True,
                        help='Path to training data (txt or json)')
    parser.add_argument('--max_seq_length', type=int, default=512,
                        help='Maximum sequence length (default: 512)')
    parser.add_argument('--validation_split', type=float, default=0.1,
                        help='Validation split ratio (default: 0.1)')
    
    # Training arguments
    parser.add_argument('--output_dir', type=str, default='./output',
                        help='Output directory (default: ./output)')
    parser.add_argument('--num_train_epochs', type=int, default=3,
                        help='Number of training epochs (default: 3)')
    parser.add_argument('--batch_size', type=int, default=4,
                        help='Batch size per device (default: 4)')
    parser.add_argument('--gradient_accumulation_steps', type=int, default=1,
                        help='Gradient accumulation steps (default: 1)')
    parser.add_argument('--learning_rate', type=float, default=5e-5,
                        help='Learning rate (default: 5e-5)')
    parser.add_argument('--weight_decay', type=float, default=0.01,
                        help='Weight decay (default: 0.01)')
    parser.add_argument('--warmup_ratio', type=float, default=0.1,
                        help='Warmup ratio (default: 0.1)')
    parser.add_argument('--lr_scheduler', type=str, default='cosine',
                        choices=['linear', 'cosine', 'constant', 'polynomial'],
                        help='Learning rate scheduler type (default: cosine)')
    parser.add_argument('--fp16', action='store_true',
                        help='Use FP16 mixed precision')
    parser.add_argument('--bf16', action='store_true',
                        help='Use BF16 mixed precision')
    parser.add_argument('--gradient_checkpointing', action='store_true',
                        help='Use gradient checkpointing')
    parser.add_argument('--save_steps', type=int, default=500,
                        help='Save checkpoint every X steps (default: 500)')
    parser.add_argument('--logging_steps', type=int, default=10,
                        help='Log every X steps (default: 10)')
    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed (default: 42)')
    
    args = parser.parse_args()
    
    # Set random seeds
    torch.manual_seed(args.seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(args.seed)
    
    print("=" * 60)
    print("LLM Training Script")
    print("=" * 60)
    print(f"Model: {args.model_name}")
    print(f"Data: {args.data_path}")
    print(f"Output: {args.output_dir}")
    print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    print("=" * 60)
    
    # Load tokenizer
    print("\nLoading tokenizer...")
    tokenizer_kwargs = {
        'cache_dir': args.cache_dir,
        'use_fast': True,
        'revision': 'main',
        'trust_remote_code': args.trust_remote_code,
    }
    
    tokenizer = AutoTokenizer.from_pretrained(
        args.tokenizer_name if args.tokenizer_name else args.model_name,
        **tokenizer_kwargs
    )
    
    # Set pad token if not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        print(f"Set pad token to EOS token: {tokenizer.pad_token}")
    
    # Load model
    print("\nLoading model...")
    model_kwargs = {
        'cache_dir': args.cache_dir,
        'revision': 'main',
        'trust_remote_code': args.trust_remote_code,
    }
    
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        **model_kwargs
    )
    
    # Enable gradient checkpointing if requested
    if args.gradient_checkpointing:
        model.gradient_checkpointing_enable()
        print("Gradient checkpointing enabled")
    
    # Resize embeddings if needed
    if len(tokenizer) > model.get_input_embeddings().weight.shape[0]:
        model.resize_token_embeddings(len(tokenizer))
        print(f"Resized token embeddings to {len(tokenizer)}")
    
    print(f"Model parameters: {model.num_parameters():,}")
    
    # Load and preprocess data
    print("\nLoading and preprocessing data...")
    train_dataset, eval_dataset = load_and_preprocess_data(
        data_path=args.data_path,
        tokenizer=tokenizer,
        max_seq_length=args.max_seq_length,
        validation_split=args.validation_split
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # False for causal LM
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        overwrite_output_dir=True,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type=args.lr_scheduler,
        fp16=args.fp16,
        bf16=args.bf16,
        save_steps=args.save_steps,
        logging_steps=args.logging_steps,
        save_total_limit=3,
        save_strategy='steps',
        evaluation_strategy='steps' if eval_dataset is not None else 'no',
        eval_steps=args.save_steps,
        load_best_model_at_end=True,
        metric_for_best_model='eval_loss',
        greater_is_better=False,
        logging_first_step=True,
        logging_dir=os.path.join(args.output_dir, 'logs'),
        report_to=[],  # Disable wandb/tensorboard unless configured
        seed=args.seed,
        dataloader_num_workers=4,
        remove_unused_columns=False,
    )
    
    # Initialize trainer
    print("\nInitializing trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=data_collator,
        callbacks=[LoggingCallback()],
    )
    
    # Train
    print("\nStarting training...")
    print("=" * 60)
    
    trainer.train()
    
    # Save final model
    print("\nSaving final model...")
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    
    print("\n" + "=" * 60)
    print("Training completed successfully!")
    print(f"Model saved to: {args.output_dir}")
    print("=" * 60)


if __name__ == '__main__':
    main()
