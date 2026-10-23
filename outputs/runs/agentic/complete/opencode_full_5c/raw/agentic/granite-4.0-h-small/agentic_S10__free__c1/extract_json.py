import json
from model_client import create_client


def extract_json(text: str, model: str = "gpt-4o-mini") -> dict:
    """Extract structured JSON from text using a hosted LLM.

    Args:
        text (str): The text containing structured data.
        model (str): The model family to use (default: gpt-4o-mini).

    Returns:
        dict: The parsed JSON object.
    """
    client = create_client(model)
    prompt = f"Extract structured JSON from the following text. Return only the JSON, no explanations:\n\n{text}"
    response = client.chat_completion(messages=[{"role": "user", "content": prompt}])
    json_str = response.choices[0].message.content.strip()
    return json.loads(json_str)
