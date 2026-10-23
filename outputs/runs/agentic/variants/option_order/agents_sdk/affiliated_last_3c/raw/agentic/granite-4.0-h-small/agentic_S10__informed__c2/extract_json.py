import os
import json
from model_client import get_llm_client
from model_models import LLMRequest, LLMResponse

def extract_json(text: str, model_family: str = "gpt-4") -> dict:
    """Extract structured JSON from text using a hosted LLM.

    Args:
        text (str): The input text containing data to extract.
        model_family (str): Identifier for the LLM model family.

    Returns:
        dict: Parsed JSON object.
    """
    client = get_llm_client(model_family)
    request = LLMRequest(
        prompt=f"Extract the following information as JSON from the text below (do not add any explanation):\n\n{text}\n\nReturn only valid JSON:",
        model=model_family,
        temperature=0.0,
        max_tokens=512,
    )
    response = client.chat_completion(request)
    # simple validation to ensure valid JSON
    raw = str(response.choices[0].message.content).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        raise ValueError("Model returned invalid JSON")
    return data

if __name__ == "__main__":
    sample = "User bought 3 apples, price $0.5 each, date 2025-08-01."
    print(extract_json(sample, model_family="gpt-4"))