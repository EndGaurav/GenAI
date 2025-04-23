from google import genai
from dotenv import load_dotenv
from google.genai import types
import json
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT= """
    You are an AI assistant who is expert in breaking down complex problems and then resolve the user query.
    For the given user input, analyse the input and break down the problem step by step.
    Atleast think 5-6 steps on how to solve the problem before solving it down.
    The steps are you get a user input, you analyse, you think, you again think for several times and then return an output with explanation and then finally you validate the output as well before giving final result.
    
    Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result". 

    Rules: 
    1. Follow the strict JSON output as per Output schema.
    2. Always perform one step at a time and wait for next output.
    3. Carefully analyse user query
    
    Output Format:
    {{ step: "string", content: "string" }}
    
    Example:
    User: what is 2 + 2 ?
    Assistant: {{ step: "analyse", content: "Alright! The user is interested in maths query and he is asking a basic arithmetic operations."}}
    Assistant: {{ step: "think", content: "To perform the addition i must go left to right and add all the operands." }}
    Assistant: {{ step: "output", content: 4 }}
    Assistant: {{ step: "validate", content: "seems like 4 is correct answer for 2 + 2" }}
    Assistant: {{ step: "result", content: "2 + 2 = 4 and that is calculated by adding all operands" }}

    User: what is 3 + 4  ?
    
     
"""
response = client.models.generate_content(
    model="gemini-2.0-flash-001", 
    contents= [
        {"role": "user", "parts": [{"text": f"{SYSTEM_PROMPT}"}]},
        {"role": "model", "parts": [{"text": { "step": "analyse", "content": "The user is asking for the sum of two numbers, 3 and 4. This requires basic arithmetic addition." }}]}
    ],
)

print(response.text)