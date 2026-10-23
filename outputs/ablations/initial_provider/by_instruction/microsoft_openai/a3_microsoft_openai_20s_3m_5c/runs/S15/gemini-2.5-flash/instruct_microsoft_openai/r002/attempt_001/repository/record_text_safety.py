import os
from openai import OpenAI
from typing import List, Dict, Any

def check_text_safety(text: str) -> Dict[str, Any]:
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    
    client = OpenAI(api_key=openai_api_key)
    
    response = client.moderations.create(input=text)
    
    return response.model_dump()
