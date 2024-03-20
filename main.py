from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from normalizer import normalize

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load the pre-trained model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("csebuetnlp/banglat5", use_fast=True) 
model = AutoModelForSeq2SeqLM.from_pretrained("Soyeda10/BanglishToBangla") 

# Request body model
class TextInput(BaseModel):
    text: str

# Define translation route
@app.post("/translation/")
async def translation_text(text_input: TextInput):
    user_input = text_input.text
    input_ids = tokenizer(normalize(user_input), padding=True, truncation=True, max_length=128, return_tensors="pt").input_ids
    generated_tokens = model.generate(input_ids, max_new_tokens=128)  # Set max_new_tokens to control generation length
    decoded_tokens = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return {"translation": decoded_tokens}

# Serve index.html
@app.get("/", response_class=FileResponse)
async def get_index():
    return FileResponse("static/index.html")