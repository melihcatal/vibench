import json
from model_client import ModelClient


def extract_json(text: str, model_name: str = "gpt-4o-mini") -> dict:
    """Extract structured JSON from text using a hosted LLM.

    Args:
        text (str): The source text containing structured data.
        model_name (str): Hosted model identifier (default: gpt-4o-mini).

    Returns:
        dict: Parsed JSON object.
    """
    client = ModelClient(model_name)
    prompt = f"Extract the following information as JSON, preserving structure and types. Only return valid JSON:\n\n{text}"
    response = client.complete(prompt)
    # Attempt to decode the response as JSON, raising if malformed.
    return json.loads(response["text"].strip())
