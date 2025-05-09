from _02_hello_langgraph import create_chat_graph
from dotenv import load_dotenv
from langgraph.checkpoint.mongodb import MongoDBSaver
import os 
import json
from langgraph.types import Command

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_URI = MONGODB_URI
config = {"configurable": {"thread_id": "5"}}

def init():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongodb = create_chat_graph(checkpointer=checkpointer)
       
            
        state = graph_with_mongodb.get_state(config=config)
        # print(state.values.get("messages"))
        # for message in state.values.get("messages"):
            # message.pretty_print()
            
        last_message = state.values["messages"][-1]
        print(last_message)
        tool_calls = last_message.tool_calls
        # print("Tool calls: ",tool_calls)
        user_query = None
        for call in tool_calls:
            if call.get("name") == "human_assistance":
                args = call.get("args", "{}").get("query", "")
                # print(args)
                user_query = args
                # try:
                #    args_dict = json.loads(args)
                #    user_query = args_dict.get("query")
                # except json.JSONDecodeError:
                #     print("Failed to decode function argument")
        
        print("User is trying to ask: ",user_query)
        answer = input("Resolution >> ")
        human_command = Command(resume={"data": answer})
        print("line 42 -> Human Command: ", human_command)
        events = graph_with_mongodb.stream(human_command, config, stream_mode="values")
        for event in events:
            if "messages" in event:
                event["messages"][-1].pretty_print()
                
init()