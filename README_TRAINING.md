# LLM Training Script

A comprehensive Python script for training/fine-tuning Large Language Models (LLMs) using Hugging Face Transformers and PyTorch.

## Features

- **Multiple Model Support**: Works with GPT-2, LLaMA, and other causal language models from Hugging Face
- **Flexible Data Loading**: Supports both plain text (.txt) and JSON formats
- **Memory Efficient**: 
  - Gradient checkpointing
  - Mixed precision training (FP16/BF16)
  - Gradient accumulation
- **Training Optimization**:
  - Multiple learning rate schedulers (linear, cosine, constant, polynomial)
  - Warmup ratio
  - Weight decay
- **Checkpoint Management**: Automatic saving of best model based on validation loss
- **Comprehensive Logging**: Real-time training metrics

## Installation

```bash
pip install torch transformers datasets accelerate
```

## Usage

### Basic Example

```bash
python train_llm.py --data_path your_data.txt --model_name gpt2
```

### Advanced Example

```bash
python train_llm.py \
    --model_name gpt2 \
    --data_path training_data.json \
    --output_dir ./my_model \
    --num_train_epochs 5 \
    --batch_size 8 \
    --learning_rate 2e-5 \
    --max_seq_length 1024 \
    --gradient_checkpointing \
    --fp16 \
    --warmup_ratio 0.1 \
    --lr_scheduler cosine
```

## Command Line Arguments

### Model Arguments
- `--model_name`: Model name or path (default: gpt2)
- `--config_name`: Config name or path (optional)
- `--tokenizer_name`: Tokenizer name or path (optional)
- `--cache_dir`: Cache directory for models
- `--trust_remote_code`: Trust remote code for custom models

### Data Arguments
- `--data_path`: Path to training data (txt or json) **[REQUIRED]**
- `--max_seq_length`: Maximum sequence length (default: 512)
- `--validation_split`: Validation split ratio (default: 0.1)

### Training Arguments
- `--output_dir`: Output directory (default: ./output)
- `--num_train_epochs`: Number of training epochs (default: 3)
- `--batch_size`: Batch size per device (default: 4)
- `--gradient_accumulation_steps`: Gradient accumulation steps (default: 1)
- `--learning_rate`: Learning rate (default: 5e-5)
- `--weight_decay`: Weight decay (default: 0.01)
- `--warmup_ratio`: Warmup ratio (default: 0.1)
- `--lr_scheduler`: Learning rate scheduler type [linear, cosine, constant, polynomial] (default: cosine)
- `--fp16`: Use FP16 mixed precision
- `--bf16`: Use BF16 mixed precision
- `--gradient_checkpointing`: Use gradient checkpointing
- `--save_steps`: Save checkpoint every X steps (default: 500)
- `--logging_steps`: Log every X steps (default: 10)
- `--seed`: Random seed (default: 42)

## Data Format

### Text File (.txt)
Plain text file where the entire content will be tokenized and split into chunks:

```
This is your training data. The model will learn from this text.
You can include as much text as you want in this file.
```

### JSON File (.json)
JSON file with either a list of texts or objects with 'text' field:

**Format 1 - List of strings:**
```json
[
    "First training example text.",
    "Second training example text.",
    "Third training example text."
]
```

**Format 2 - List of objects:**
```json
[
    {"text": "First training example text."},
    {"text": "Second training example text."}
]
```

**Format 3 - Dictionary with texts key:**
```json
{
    "texts": [
        "First training example text.",
        "Second training example text."
    ]
}
```

## Examples

### Fine-tune GPT-2 on Custom Text

```bash
python train_llm.py \
    --model_name gpt2 \
    --data_path my_corpus.txt \
    --output_dir ./gpt2_finetuned \
    --num_train_epochs 3 \
    --batch_size 4 \
    --learning_rate 5e-5
```

### Train with Memory Optimization

For large models or limited GPU memory:

```bash
python train_llm.py \
    --model_name meta-llama/Llama-2-7b-hf \
    --data_path dataset.json \
    --output_dir ./llama_finetuned \
    --batch_size 2 \
    --gradient_accumulation_steps 4 \
    --gradient_checkpointing \
    --fp16 \
    --max_seq_length 512
```

### Training with Validation

The script automatically splits your data into train/validation sets:

```bash
python train_llm.py \
    --model_name gpt2 \
    --data_path data.txt \
    --validation_split 0.1 \
    --output_dir ./output \
    --save_steps 100 \
    --eval_steps 100
```

## Output

After training completes, the output directory will contain:
- `pytorch_model.bin` or `model.safetensors`: Trained model weights
- `config.json`: Model configuration
- `tokenizer.json`, `tokenizer_config.json`: Tokenizer files
- `training_args.bin`: Training arguments
- `checkpoint-XXX/`: Intermediate checkpoints (if saved)
- `logs/`: Training logs

## Tips

1. **GPU Memory**: If you run out of memory:
   - Reduce `--batch_size`
   - Enable `--gradient_checkpointing`
   - Use `--fp16` or `--bf16`
   - Reduce `--max_seq_length`
   - Increase `--gradient_accumulation_steps` instead of batch size

2. **Learning Rate**: Start with a small learning rate (1e-5 to 5e-5) for fine-tuning

3. **Epochs**: For fine-tuning, 3-5 epochs is usually sufficient to avoid overfitting

4. **Validation Split**: Use 10% (0.1) for validation to monitor training progress

5. **Save Steps**: Adjust based on your dataset size - save more frequently for smaller datasets

## License

MIT License
