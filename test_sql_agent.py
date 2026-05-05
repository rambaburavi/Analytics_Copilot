from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch
import re

BASE_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
ADAPTER_PATH = "models/mistral_sql_agent_lora"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

print("Loading base model...")
model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    load_in_4bit=True,
    device_map="auto"
)

print("Loading SQL adapter...")
model = PeftModel.from_pretrained(model, ADAPTER_PATH)

prompt = """### Instruction:
Generate SQL query for the question below.

Question:
Top 5 products by total sales

### Response:
"""

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

outputs = model.generate(
    **inputs,
    max_new_tokens=120,
    do_sample=False
)

response = tokenizer.decode(outputs[0], skip_special_tokens=True)

# Extract first SQL statement only
sql_match = re.search(r"(SELECT .*?LIMIT \d+)", response, re.DOTALL)

print("\nGenerated SQL:\n")
print(sql_match.group(1) if sql_match else response)