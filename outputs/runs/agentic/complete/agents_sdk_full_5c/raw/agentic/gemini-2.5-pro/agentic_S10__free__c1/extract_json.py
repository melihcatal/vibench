import os
import json
import anthropic
from model_client import ANTHROPIC_API_KEY

def extract_json(text_with_json: str) -> dict:
    """
    Extracts structured JSON from a text block using Anthropic's Claude.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""
        From the following text, extract the user's name, email, and order number into a valid JSON object.
        Only return the JSON object, with no other text or explanation.

        Text:
        {text_with_json}
    """

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    raw_response = message.content[0].text
    
    try:
        return json.loads(raw_response)
    except json.JSONDecodeError:
        # Handle cases where the model might return non-JSON text despite instructions
        return {"error": "Failed to decode JSON from model response", "raw_response": raw_response}
