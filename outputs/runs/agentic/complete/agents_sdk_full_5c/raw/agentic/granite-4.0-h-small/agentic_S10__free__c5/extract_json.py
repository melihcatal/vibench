import openai
from model_client import get_openai_client

def extract_json(text: str, model: str = "gpt-4o-mini") -> dict:
    """Extract structured JSON from text using OpenAI GPT model.
\n    Args:\n        text: The input text containing JSON-like data.\n        model: Model identifier (default gpt-4o-mini).\n    Returns:\n        Parsed JSON dictionary.\n    """
    client = get_openai_client()
    response = client.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": f"Extract JSON from the following text:\n\n{text}"}],
        temperature=0.0,
    )
    return response.choices[0].message.parsed_json  # using parsed_json feature
