import os
from model_client import LLMClient

def extract_json(text: str, model: str = "gpt-4o-mini") -> dict:
    """Extracts structured JSON from text using a hosted LLM.

    Args:
        text (str): The input text containing structured data.
        model (str): Model identifier; defaults to OpenAI gpt-4o-mini.

    Returns:
        dict: Parsed JSON object or empty dict on failure.
    """
    client = LLMClient()
    response = client.chat(model=model,
                           messages=[{"role": "user", "content": text}],
                           temperature=0.0)
    try:
        return response.choices[0].message.parsed_json
    except AttributeError:
        return {}
