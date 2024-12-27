import tool_list
import os
from dotenv import load_dotenv
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent

load_dotenv()
COHERE_API_KEY = os.getenv('COHERE_API_KEY')
LANGCHAIN_API_KEY = os.getenv('LANGCHAIN_API_KEY')
LANGCHAIN_TRACING_V2 = "true"
LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"

tools_list = tool_list.TOOLS

with open('vision_prompt.txt', 'r') as file:
    preamble = file.read()

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


input_data = {
    'datetime':'',
    'input':'',
    'image':'',
}

import datetime
def direct_chat(user_input):
    global input_data
    input_data = {
        'datetime':str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        'input':user_input.input,
        'image':user_input.image,
    }
    response = agent_executor.invoke({"input": input_data, "preamble": preamble})['output']
    return response

with open('vision_prompt.txt', 'r') as file:
    preambleV = file.read()

def direct_image(user_input):
    image_url = user_input.image
    loc = user_input.location
    return tool_list.visual_tool.invoke({"prompt":preambleV, "image_url":image_url, "loc":loc})