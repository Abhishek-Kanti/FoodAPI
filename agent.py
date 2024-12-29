#changed:
# in input_data dictionary, new input is location.

import tool_list
import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent

load_dotenv()
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "FoodAI_tracing"
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"

tools_list = tool_list.TOOLS

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "{preamble}",),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# prompt = ChatPromptTemplate.from_template("{input}")

llm = ChatCohere(model="command-r")
agent = create_cohere_react_agent(llm, tools_list, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools_list, verbose=True)

# input_data = {           #old
#     'datetime':'',
#     'input':'',
#     'image':'',
# }

input_data = {              #new
    'image':'',
    'location':'',
}

with open('AgentImg_prompt.txt', 'r') as file:
    preamble = file.read()

import datetime
def ai_ImgAnalyser(user_input):
    global input_data
    weather_api_res = tool_list.get_current_weather(user_input.location)
    input_data = {
        'datetime':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'image':user_input.image,
        'location':user_input.location,
        'temperature':f"{weather_api_res['main']['temp']}°C",
        'humidity':f"{weather_api_res['main']['humidity']}%"
    }
    response = agent_executor.invoke({"input": input_data, "preamble": preamble})['output']
    return response

with open('AgentChat_prompt.txt', 'r') as file:
    preambleC = file.read()

def ai_InventoryManeger(user_input):
    global input_data
    input_data = {
        'datetime':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'input':user_input.input,
        'location': user_input.location,
    }
    response = agent_executor.invoke({"input": input_data, "preamble": preambleC})['output']
    return response


with open('vision_prompt.txt', 'r') as file:
    preambleV = file.read()

def direct_image(user_input):
    image_url = user_input.image
    loc = user_input.location
    return tool_list.visual_tool.invoke({"prompt":preambleV, "image_url":image_url, "loc":loc})