import json
from model_client import get_anthropic_client

MODEL_NAME = "claude-3-5-sonnet-20240620"

def extract_json(text: str) -> dict:
    """
    Extracts structured JSON from unstructured text using the Anthropic API.
    """
    client = get_anthropic_client()

    prompt = f"""
    Extract the user's name, email address, and phone number from the following text.
    Return the information as a valid JSON object with the keys "name", "email", and "phone".
    If a value is not present, use null.

    Text:
    "{text}"
    """

    try:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=512,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            system="You are an expert at extracting structured data and returning it in JSON format.",
        )
        
        if response.content and isinstance(response.content, list) and hasattr(response.content[0], 'text'):
            # The model might return the JSON inside a markdown block
            json_text = response.content[0].text
            if "```json" in json_text:
                json_text = json_text.split("```json\n")[1].split("\n```")[0]
            
            return json.loads(json_text)
        
        return {}
    except Exception as e:
        print(f"An error occurred during JSON extraction: {e}")
        return {}
