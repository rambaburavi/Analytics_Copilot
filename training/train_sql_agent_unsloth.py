from unsloth import FastLanguageModel
from datasets import load_dataset

MODEL_NAME = "unsloth/codellama-7b-instruct-bnb-4bit"
DATA_PATH = "data/sql_training_dataset.json"
OUTPUT_DIR = "models/codellama-sql-lora"

print("Loading model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_NAME,
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 8,
    target_modules = ["q_proj", "v_proj"],
    lora_alpha = 16,
    lora_dropout = 0.05,
)

print("Loading dataset...")
dataset = load_dataset("json", data_files=DATA_PATH)["train"]

def format_example(example):
    return {
        "text": f"""### Instruction:
Generate SQL query for the question below.

Question:
{example['question']}

Schema:
Database: {example['db_id']}

### Response:
{example['sql']}
"""
    }

dataset = dataset.map(format_example)

print("Training model...")

from transformers import TrainingArguments
from trl import SFTTrainer

trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = 2048,
    args = TrainingArguments(
        per_device_train_batch_size = 1,
        gradient_accumulation_steps = 4,
        num_train_epochs = 1,
        learning_rate = 2e-4,
        fp16 = True,
        logging_steps = 20,
        output_dir = OUTPUT_DIR,
    ),
)

trainer.train()

print("Saving model...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("Training complete!")