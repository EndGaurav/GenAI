from openai import OpenAI
from dotenv import load_dotenv
import requests
import os
import json
import math

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def get_weather(city_name):
    # TODO!: Do an actual API Call
    print("🔨 Tool Called: get_weather for", city_name)
    
    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={city_name}&appid={WEATHER_API_KEY}"

    response = requests.get(url)

    if response.status_code == 200:
        parsed_response = response.json()
        return f"The weather in {city_name} is {math.floor(parsed_response["main"]["temp"])}."
    return "Something went wrong"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather details"
    }
}

tool_description ="\n".join( 
    [f"      - {tool_name}: {tool_info["description"]}"  for tool_name, tool_info in available_tools.items() ]
)

SYSTEM_PROMPT = f"""
    You are an helpful AI assistant who is specialized in resolving user query.
    You work on start, plan, action, observer mode.
    For the given query and using available tools, plan the step by step execution, based on the planning.
    Select the relevant tool from the available tool. and based on the tool selection you perform an action to call the tool.
    Wait for the observation and based on the observation from the tool call resolve the user query.
    
    Rules: 
    - Follow the output json format.
    - Always perform one step at a time and wait for next input.
    - Carefully analyse the user query
    
    Output JSON format:
    {{
        "step": "string",
        "content": "string",
        "function": "The name of function if the step is action",
        "input": "The input parameter for the function"
    }}
    
    Available Tools: 
    {tool_description}
    
    Example: 
    User: What is weather of new york ?
    Output: {{ "step": "plan", "content": "The user is interested in weather data of new york" }}
    Output: {{ "step": "plan", "content": "From the available tools i should call get_weather" }}
    Output: {{ "step": "action", "function": "get_weather", "input": "new york" }}
    Output: {{ "step": "observe", "output": "12 Degree Cel" }}
    Output: {{ "step": "output", "content": "The weather for new york seems to be 12 degrees" }}
"""



messages = [
        { "role": "system", "content": SYSTEM_PROMPT }
    ]



while True:
    print("#" * 150)
    print(f"👂🏻: For closing the execution environment type following action: exit or bye")
    query = input("> ")
    if query in ("exit", "bye"):
        break
    messages.append({"role": "user", "content": query})
    
    while True: 
        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            response_format={ "type": "json_object" },
            messages=messages
        )
       
        parsed_response = json.loads(response.choices[0].message.content)
        print(f"Parsed Response: {parsed_response}")
        messages.append({"role": "assistant", "content": json.dumps(parsed_response)})

        if parsed_response.get("step") == "plan":
            print(f"🧠: {parsed_response.get("content")}")
            continue
        
        if parsed_response.get("step") == "action":
            function_name = parsed_response.get("function")
            function_input = parsed_response.get("input")

            if available_tools.get(function_name, False) != False:
                output = available_tools[function_name].get("fn")(function_input)
                messages.append({"role": "assistant", "content": json.dumps({"step":"observe", "content":output})})
                continue
            
        if parsed_response.get("step") == "output":
            print(f"🤖: {parsed_response.get("content")}")
            break

