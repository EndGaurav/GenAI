from openai import OpenAI
import requests
from dotenv import load_dotenv
import json
load_dotenv()

client =  OpenAI()

def get_weather(city_name):
    # TODO!: Do an actual API Call
    print("🔨 Tool Called: get_weather", city_name)
    
    url = f"https://wttr.in/{city_name}?format=%C+%t"
    response = requests.get(url)

    if response.status_code == 200:
        return f"The weather in {city_name} is {response.text}."
    return "Something went wrong"

available_tools = {
    "get_weather": {
        "fn": get_weather,
        "description": "Takes a city name as an input and returns the current weather details"
    }
}

tool_description = "\n".join(
    [f"     - {tool_name}: {tool_info['description']}" for tool_name, tool_info in available_tools]
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

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

while True:
    user_query = input("> ")
    messages.append({"role": "user", "content": user_query})
    
    while True: 
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages
        )
    
        # must check the type of below response 
        parsed_output = json.load(response.choices[0].message.content)
        messages.append({"role": "assistant", "content": json.dumps(parsed_output)})
        
        if parsed_output.get("step") == "plan":
            print(f"🧠: {parsed_output.get("content")}")
            continue
        
        if parsed_output.get("step") == "action":
            tool_name = parsed_output.get("function")
            tool_input = parsed_output.get("input")
            
            if available_tools.get(tool_name, False) != False:
                output = available_tools[tool_name].get("fn")(tool_input)
                messages.append({"role": "assistant", "content": json.dumps({"step": "observe", "output": output})})
                continue
            
        if parsed_output.get("step") == "output":
            print(f"🤖: {parsed_output.get("content")}")
            break
        
