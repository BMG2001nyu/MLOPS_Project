from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from peft import LoraConfig, get_peft_model
from datasets import load_dataset

# Load QA dataset
dataset = load_dataset("squad_v2")  # Replace with your lecture QA pairs later

# Load the base Phi-3.5 Mini Instruct model
model_name = "microsoft/phi-2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto")

# Apply LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, lora_config)

# Preprocessing
def preprocess_function(examples):
    questions = ["Answer: " + q for q in examples["question"]]
    contexts = examples["context"]
    inputs = [c + " " + q for c, q in zip(contexts, questions)]
    model_inputs = tokenizer(inputs, max_length=1024, truncation=True)
    labels = tokenizer(examples["answers"]["text"], max_length=128, truncation=True)
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Training arguments
training_args = TrainingArguments(
    output_dir="./qa_model",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    num_train_epochs=1,
    save_steps=500,
    logging_dir="./logs",
    fp16=True,
    evaluation_strategy="steps",
    eval_steps=500,
)

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)

# Train
trainer.train()

# Save model
model.save_pretrained("./qa_model")
tokenizer.save_pretrained("./qa_model")
