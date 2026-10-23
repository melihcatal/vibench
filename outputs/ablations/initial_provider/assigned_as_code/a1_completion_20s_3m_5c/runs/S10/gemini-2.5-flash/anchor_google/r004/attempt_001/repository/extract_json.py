import os
from google import genai
from model_client import get_gemini_client

def extract_json(payload, config=None):
    config = config or {}
    text = payload["text"]
    format_instructions = payload.get("format_instructions", "Extract the relevant information as a JSON object.")

    prompt = f"""{format_instructions}

Here is the text:
{text}

Please respond with only the JSON object.
"""

    client = get_gemini_client(api_key=config.get("api_key"))
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    
    # Attempt to parse the response as JSON. If it fails, return the raw text.
    try:
        import json
        return {"json_output": json.loads(response.text.strip())}
    except json.JSONDecodeError:
        return {"json_output": response.text.strip()}
