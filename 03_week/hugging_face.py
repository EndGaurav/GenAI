import os 
from dotenv import load_dotenv
from transformers import AutoTokenizer,  AutoModelForCausalLM, pipeline
import torch

load_dotenv()

model_name = "google/gemma-3-1b-it"

tokenizer = AutoTokenizer.from_pretrained(model_name)
print(tokenizer("Hello world"))

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16 
)



gen_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

gen_pipeline("Where is dehradun ?")









