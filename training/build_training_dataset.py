from datasets import load_dataset
import json
import os

print("Loading Spider dataset...")

dataset = load_dataset("spider")

train_data = dataset["train"]

formatted_data = []

print("Building schema-aware dataset...")

for row in train_data:

    db_id = row["db_id"]
    question = row["question"]
    sql = row["query"]

    # Since schema metadata isn't available in this loader,
    # we store db_id as schema reference placeholder

    formatted_data.append({
        "db_id": db_id,
        "schema": f"Database ID: {db_id}",
        "question": question,
        "sql": sql
    })


os.makedirs("data", exist_ok=True)

with open("data/sql_training_dataset.json", "w", encoding="utf-8") as f:
    json.dump(formatted_data, f, indent=2)


print("Dataset created successfully")
print("Total samples:", len(formatted_data))