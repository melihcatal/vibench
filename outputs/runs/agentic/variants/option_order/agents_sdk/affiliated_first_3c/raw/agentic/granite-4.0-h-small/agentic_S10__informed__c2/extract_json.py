import os
from model_client import get_llm_client
from model_models import sanitize_response

def extract_json(text: str) -> dict:
    """Extract structured JSON from text using a hosted LLM (OpenAI GPT-3.5 Turbo).
    Returns a Python dict representing the parsed JSON.
    """
    client = get_llm_client()
    prompt = f"Extract the following information as valid JSON. Only return JSON, no explanations:\n    {text}"
    response = client.chat_completion(messages=[{"role": "user", "content": prompt}])
    raw = sanitize_response(response['choices'][0]['message']['content'])
    # Simple safety to avoid non-JSON output
    try:
        import json
        return json.loads(raw)
    except Exception:
        raise ValueError("LLM did not return valid JSON")
