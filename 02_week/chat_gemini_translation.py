from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyC-01BBVnNKx1kwsRwa8rs5OszOTDuzP_A')

SYSTEM_PROMPT = '''
    You are an AI assistant who is specialized in garwali uttrakhand boli or languages.
    Whenever user provide you a query to do something in garwali you will gracefully handle it. 
    And provide response in hindi which is written using english character.
    
    User: Write a song in garwali for my lover who lives in saud gaao ?
   
    '''

response = client.models.generate_content(
    model="gemini-2.0-flash-001", 
    contents= f"{SYSTEM_PROMPT}"
)

print(response.text)