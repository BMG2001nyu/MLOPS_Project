from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

app = FastAPI()

# Load summarization model
base_model = "mistralai/Mistral-7B-Instruct-v0.2"
model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto")
model = PeftModel.from_pretrained(model, "./summarizer_model")
tokenizer = AutoTokenizer.from_pretrained(base_model)
model.eval()

class SummarizationRequest(BaseModel):
    text: str

@app.post("/summarize")
async def summarize(request: SummarizationRequest):
    try:
        inputs = tokenizer(request.text, return_tensors="pt", truncation=True, max_length=4096)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        summary_ids = model.generate(**inputs, max_new_tokens=200)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
