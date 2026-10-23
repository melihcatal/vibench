import os
from model_client import get_chat_client
from model_models import format_chat_response

def extract_json(prompt: str, model: str = "gpt-4o") -> dict:
    """Extract structured JSON from text using a hosted LLM.

    Args:
        prompt (str): Prompt that instructs the model to produce JSON.
        model (str): Model identifier (default GPT-4o).
    Returns:
        dict: Parsed JSON object.
    """
    client = get_chat_client(model)
    response = client.chat(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return format_chat_response(response, as_json=True)
