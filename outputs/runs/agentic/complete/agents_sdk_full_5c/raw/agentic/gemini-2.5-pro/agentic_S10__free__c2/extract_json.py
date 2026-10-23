import json
from model_client import get_cohere_client

def extract_user_info(text: str) -> dict:
    """
    Extracts structured user information (name, email) from text into JSON.
    """
    client = get_cohere_client()
    
    preamble = """
    ## Task and Context
    You are an expert JSON extractor. Your task is to extract the user's name and email from the provided text.
    You must output a single, valid JSON object and nothing else. Do not include any commentary or markdown formatting.

    ## Schema
    {
      "name": "string",
      "email": "string"
    }
    """

    response = client.chat(
        model="command-r",
        preamble=preamble,
        message=f"Extract the user information from this text: '{text}'"
    )
    
    try:
        # The model is instructed to only return JSON
        extracted_json = json.loads(response.text)
        return extracted_json
    except json.JSONDecodeError:
        # Handle cases where the model might not have returned perfect JSON
        return {"error": "Failed to decode JSON from model response", "raw_text": response.text}
