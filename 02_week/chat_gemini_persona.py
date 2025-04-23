from google import genai
from dotenv import load_dotenv
from google.genai import types
import json
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


while True:
    
    query = input("> ")
    
    if query.lower() in ["bye", "exit", "quit"]:
        print("Hanji chalo milte hai phir! 👋🏻")
        break

    SYSTEM_PROMPT= f"""
        You are a hitesh choudhary who has a two youtube channel and one is hitesh choudhary and second is chai aur code.
        And whenever he starts communicating with anyone he always used one word that is known as hanji.
        He loves chai very much and he has a taste of every type of chai. 
        Now whenever any user ask you anything response it in hitesh choudhary way.
        
        User: {query} 
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents= f"{SYSTEM_PROMPT}"
    )

    print(response.text)