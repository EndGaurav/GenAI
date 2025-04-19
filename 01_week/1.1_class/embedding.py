from dotenv import load_dotenv
# import google.generativeai as genai 
from google import genai
import os
load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",
)

print(response.text)




