import json
import os
from model_client import HostedModelClient


def extract_json(text: str, model: str = "gpt-4o") -> dict:
    """Extracts structured JSON data from text using a hosted LLM.

    Args:
        text: The text containing structured data.
        model: Model identifier for the hosted LLM provider.

    Returns:
        Parsed JSON data extracted from the input text.
    """
    client = HostedModelClient(model=model)
    payload = {
        "prompt": f"Extract structured JSON from the following text:\n{text}",
        "temperature": 0.0,
        "max_tokens": 500,
    }
    response = client.chat_completion(payload)
    content = response["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("Failed to parse JSON from model output")
