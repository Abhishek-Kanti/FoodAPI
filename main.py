#changed:
# in input_data_chat class, 'input' and 'image' input types now can be none and new key val pair of 'location' is added.

import json
from fastapi import FastAPI
from pydantic import BaseModel
from agent import ai_ImgAnalyser ,ai_InventoryManeger ,direct_image
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class input_data_ai_ImgAnalyser(BaseModel):
    image: str|None
    location: str|None

class input_data_ai_InventoryManeger(BaseModel):
    input: str|None
    location: str|None

class input_data_vision(BaseModel):
    image: str
    location: str

@app.get("/")
async def confirmation():
    return {"message":"API working!"}


@app.post("/ai_ImgAnalyser")
async def model1(input: input_data_ai_ImgAnalyser):
    response = ai_ImgAnalyser(input)
    try:
        # Extract the JSON portion from the response string
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        if start_idx != -1 and end_idx != -1:
            json_part = response[start_idx:end_idx + 1]
            # Convert JSON string to a dictionary
            meta_data = json.loads(json_part)
            # Remove the JSON part from the original response
            response_without_json = response.replace(json_part, '').strip()
            # Use rpartition to split at the last occurrence of '\n'
            response_without_json, _, _ = response_without_json.rpartition('\n')
        else:
            raise ValueError("No valid JSON found in the response.")

        return {
            "response": response_without_json,
            "meta_data": meta_data
        }
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON: {e}")
    # return {"response": response}    


@app.post("/direct_img")
async def model2(input: input_data_vision):
    response = direct_image(input)
    try:
        # Extract the JSON portion from the response string
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        if start_idx != -1 and end_idx != -1:
            json_part = response[start_idx:end_idx + 1]
            # Convert JSON string to a dictionary
            meta_data = json.loads(json_part)
            # Remove the JSON part from the original response
            response_without_json = response.replace(json_part, '').strip()
            # Use rpartition to split at the last occurrence of '\n'
            response_without_json, _, _ = response_without_json.rpartition('\n')
        else:
            raise ValueError("No valid JSON found in the response.")

        return {
            "response": response_without_json,
            "meta_data": meta_data
        }
    except json.JSONDecodeError as e:
        raise ValueError(f"Error parsing JSON: {e}")
    # return {"response": response}

@app.post("/ai_InventoryManeger")
async def model3(input: input_data_ai_InventoryManeger):
    response = ai_InventoryManeger(input)
    return {"response": response}