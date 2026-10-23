# [SAME-SCENARIO] extract_json.py

import json
import os
from model_client import HostedLLMClient

def extract_json(text: str, model_family: str = "gpt-4") -> dict:
    """Extract structured JSON from text using a hosted LLM.

    Args:
        text (str): Input text containing data to extract.
        model_family (str): Identifier for the provider.

    Returns:
        dict: Parsed JSON object.
    """
    client = HostedLLMClient(model_family=model_family)
    system_prompt = (
        "You are an AI that extracts structured JSON from unstructured text."
        " Respond ONLY with valid JSON, no extra text."
    )
    prompt = f"{system_prompt}\n\n{text}"
    response = client.complete(prompt=prompt)
    try:
        return json.loads(response['choices'][0]['text'].strip())
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from model")
