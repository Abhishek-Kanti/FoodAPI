import os
import json
import requests
from datetime import datetime

from PIL import Image
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from langchain_community.tools.tavily_search import TavilySearchResults

import base64
import httpx


load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

web_search_tool = TavilySearchResults()
web_search_tool.name = "Web_Search"
web_search_tool.description = "Retrieve relevant info from web."

class web_search_inputs(BaseModel):
   query: str = Field(description="query for searching on web")

web_search_tool.args_schema = web_search_inputs

def get_current_weather(city_name):
    if not WEATHER_API_KEY:
        raise ValueError("WEATHER_API_KEY environment variable is not set.")
    
    # Construct the API URL
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric"
    
    # Make the API request
    response = requests.get(url)
    
    # Raise an exception if the request fails
    if response.status_code != 200:
        raise Exception(f"API call failed: {response.status_code}, {response.text}")
    
    # Parse and return the JSON response
    return response.json()

@tool
def visual_tool(prompt: str, image_url: str, loc: str) -> str:
    """Responding on image url input and location
    Args:
        prompt (str): prompt input
        image_url (str): url input
        loc (str): location input
    """
    # Get current date and time
    now = datetime.now()
    user_city = loc #only city
    weather_api_res = get_current_weather(user_city)
    temp_and_humi = f"Temperature: {weather_api_res['main']['temp']}°C\nHumidity: {weather_api_res['main']['humidity']}%"
    response = requests.get(image_url)
    if response.status_code == 200:
        pass
    else:
        return(f"Error fetching image. Status code: {response.status_code}")

    image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt+"\n"+str(now)+"\n"+temp_and_humi},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
    try:
        response = model.invoke([message])
        print("Respond succesfully: ", response.content)
        return response.content
    except Exception as e: 
        print("Error found : ",e)
        return e

visual_tool.name = "visual"
visual_tool.description = "Get image details on given prompt"

class visual_inputs(BaseModel):
   prompt: str = Field(description="prompt for image")
   image_url: str = Field(description="url for image")
   loc: str = Field(description="geographical location of the image")
visual_tool.args_schema = visual_inputs

TOOLS = [web_search_tool, visual_tool]