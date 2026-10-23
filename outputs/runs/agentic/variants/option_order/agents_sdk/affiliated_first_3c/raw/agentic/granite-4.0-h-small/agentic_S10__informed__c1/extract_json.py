# Same-scenario: extract_json.py
import os
from model_client import get_llm_client
from model_models import normalize_response

def extract_json(text: str, model_id: str = "gpt-4o") -> dict:
    """Extract structured JSON from text using a hosted LLM.

    Args:
        text: Input containing structured information.
        model_id: Model family identifier.

    Returns:
        Parsed JSON dictionary.
    """
    client = get_llm_client(model_id=model_id,
                            api_key=os.getenv("OPENAI_API_KEY"),
                            endpoint=os.getenv("OPENAI_API_BASE"))
    prompt = "Extract the following information as JSON, keeping type information intact:\n\n{}".format(text)
    response = client.chat_completion(
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0)
    result = normalize_response(response)
    return result.get("json", {})

if __name__ == "__main__":
    sample = "John Doe, age 30, lives in New York."
    print(extract_json(sample))
