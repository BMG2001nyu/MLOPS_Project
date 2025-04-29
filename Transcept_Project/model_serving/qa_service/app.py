from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

app = FastAPI()

# Load QA model
base_model = "microsoft/phi-2"
model = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto")
model = PeftModel.from_pretrained(model, "./qa_model")
tokenizer = AutoTokenizer.from_pretrained(base_model)
model.eval()

class QARequest(BaseModel):
    context: str
    question: str

@app.post("/answer")
async def answer(request: QARequest):
    try:
        prompt = f"{request.context}\nQuestion: {request.question}\nAnswer:"
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=4096)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        answer_ids = model.generate(**inputs, max_new_tokens=150)
        answer = tokenizer.decode(answer_ids[0], skip_special_tokens=True)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}
