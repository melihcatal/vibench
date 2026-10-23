import json
import os
from typing import Dict, Any, List
from mistralai.client import MistralClient

def message_summary(results: List[Dict[str, Any]]) -> str:
    """
    Summarizes message processing results using Mistral Chat API.
    """
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEY environment variable is required.")
    
    client = MistralClient(api_key=api_key)
    
    prompt = f"Summarize the following message processing results in a concise paragraph:\\n{json.dumps(results, indent=2)}"
    
    response = client.chat(
        model="mistral-large-latest",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content