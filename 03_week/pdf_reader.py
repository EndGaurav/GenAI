import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv
import os
from pdfminer.high_level import extract_text


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Ask for the file path
user_file_path = input("Enter the path to your file: ")

def extract_txt():
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        print(len(reader.pages))
        for i, page in enumerate(reader.pages):
            print(f"--- Page {i + 1} ---")
            # print(page.extract_text())
            return page.extract_text()



SYSTEM_PROMPT = f"""
    You are an AI assistant who is specialized in reponding a query very gracefully.
    {extract_txt()} this is complete text repond user only related to this text context. 
"""

while True: 
    query = input("User: ")
    response = client.chat.completions.create(
                model="gemini-2.0-flash",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": query}
                ]
            )
    print(response.choices[0].message.content)
    
    if query in ["exit", "bye"]:
        break

       