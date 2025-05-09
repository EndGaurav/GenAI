from mem0 import Memory
from openai import OpenAI
from dotenv import load_dotenv
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


QUADRANT_HOST = "localhost"
NEO4J_URI=os.getenv("NEO4J_URI")
NEO4J_USERNAME=os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD=os.getenv("NEO4J_PASSWORD")

config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": QUADRANT_HOST,
            "port": 6333,
            "embedding_model_dims":768
        }
    },
    "llm": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_API_KEY,
            "model": "gemini-2.0-flash-001"
        }
    },
    "embedder": {
        "provider": "gemini",
        "config": {
            "api_key": GEMINI_API_KEY,
            "model": "models/text-embedding-004",
            "embedding_dims":768
        }
    },
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": NEO4J_URI,
            "username": NEO4J_USERNAME,
            "password": NEO4J_PASSWORD
        }
    },
    "version": "v1.1",
}

mem_client = Memory.from_config(config)

client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def chat(message):
    
    releated_memories = mem_client.search(message, user_id="user_one")

    # print("Memory: ", releated_memories)

    memories = "\n".join([ m["memory"] for m in releated_memories.get("results") ])
    
    # print(memories)
    
    SYSTEM_PROMPT = f"""
    You are an AI assistant who just answer related to my query and you are aware of my past interactions and also i will pass my memories to you for better context availability. 
    {memories}
    """
    
    messages = [
        
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": message }
    ]
    
    response = client.chat.completions.create(
        model="gemini-2.0-flash-001",
        messages=messages
    )
    
    messages.append({ "role": "assistant", "content": response.choices[0].message.content })
    
    mem_client.add(messages, user_id="user_one")
    
    return response.choices[0].message.content


while True:
    message = input("> ")
    
    if message in ["exit"]:
        break
    print("🤖: ",chat(message))