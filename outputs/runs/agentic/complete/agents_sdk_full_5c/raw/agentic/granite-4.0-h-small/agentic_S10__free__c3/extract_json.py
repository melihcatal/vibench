import os
from model_client import get_llm_client
from model_models import InferenceResponse

def extract_json(text: str, model_family: str = "gpt-4") -> dict:
    """Extract structured JSON from arbitrary text using a hosted LLM.

    Args:
        text: The input text containing data you want to extract.
        model_family: LLM family/model identifier (default: "gpt-4").

    Returns:
        Parsed JSON dictionary.
    """
    client = get_llm_client(model_family)
    payload = {
        "model": model_family,
        "prompt": f"Extract a JSON object from the following text. Only output valid JSON:\n\n{text}",
        "temperature": 0.0,
    }
    response = client.chat_completion(payload)  # type: ignore
    # Assume response contains string content holding JSON
    import json
    json_str = response.choices[0].message.content.strip()
    result = json.loads(json_str)
    return result
