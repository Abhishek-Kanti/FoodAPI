import json
from fastapi import FastAPI
from pydantic import BaseModel
from agent import direct_chat, direct_image

app = FastAPI()

class input_data_chat(BaseModel):
    datetime: str
    input: str
    image: str

class input_data_vision(BaseModel):
    image: str
    location: str

@app.get("/")
async def confirmation():
    return {"message":"API working!"}

@app.post("/direct_chat")
async def model2(input: input_data_chat):
    response = direct_chat(input)
    return {"response": response}

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