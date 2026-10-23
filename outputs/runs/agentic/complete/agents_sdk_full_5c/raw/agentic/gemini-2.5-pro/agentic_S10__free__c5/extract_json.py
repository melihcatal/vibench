import json
from typing import Dict, Any
from model_client import client

def extract_structured_json(text_with_data: str) -> Dict[str, Any]:
    """
    Calls a Cohere model to extract a structured JSON object from a text string.
    """
    preamble = """
    ## Task and Context
    You are an expert JSON extractor. Your task is to extract a structured JSON object 
    from the user's message. The JSON object should represent the key entities and 
    their relationships mentioned in the text. Only output the JSON object, nothing else.
    """
    
    response = client.chat(
        preamble=preamble,
        message=f"Here is the text to extract JSON from: '{text_with_data}'",
        model="command-r-plus",
        temperature=0.0,
    )

    # The model response is expected to be a string containing only the JSON
    json_string = response.text.strip()
    
    # Clean up markdown fences if the model adds them
    if json_string.startswith("```json"):
        json_string = json_string[7:]
    if json_string.endswith("```"):
        json_string = json_string[:-3]

    return json.loads(json_string)
