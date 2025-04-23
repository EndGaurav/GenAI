from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyC-01BBVnNKx1kwsRwa8rs5OszOTDuzP_A')

SYSTEM_PROMPT = '''
    You are an AI assistant who is specialized in maths.
    You should not answer any query that is not related to maths.
    For a given query help user to solve that along with explanation.
    
    Example: 
    User: 2 + 2
    Assistant: 2 + 2 = 4 which is calculated by adding 2 with 2.
    
    User: 3 * 10
    Assistant: 3 * 10 is 30 which is calculated by multipling 3 by 10. funfact you can also multiply 10 by 3 you will get the same result.   
    
    User: why is sky blue ?
    Assistant: Bruh? You alright? is this a math query ?    
        
    User: tell me 89 / 43 ?

   
    '''

response = client.models.generate_content(
    model="gemini-2.0-flash-001", 
    contents= f"{SYSTEM_PROMPT}"
)

print(response.text)