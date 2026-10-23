# extract_json.py
# [SAME-SCENARIO]
"""Calls a hosted LLM to extract structured JSON from arbitrary text."""

from model_client import LLMClient


def extract_json(text: str, model: str = "gpt-4o-mini") -> dict:
    """Extracts JSON from the provided text using the specified hosted model.

    Args:
        text (str): The text containing JSON to be extracted.
        model (str): Identifier of the hosted model to use.
    Returns:
        dict: Parsed JSON object.
    """
    client = LLMClient(model=model)
    prompt = f"Extract the JSON structure from the following snippet and return it as a JSON object (no explanation):\n\n{text}"
    response = client.chat(messages=[{"role": "user", "content": prompt}])
    # Assumes response is a JSON string wrapped in quotes; parse it safely
    import json

    json_str = response["choices"][0]["message"]["content"].strip()
    return json.loads(json_str)
