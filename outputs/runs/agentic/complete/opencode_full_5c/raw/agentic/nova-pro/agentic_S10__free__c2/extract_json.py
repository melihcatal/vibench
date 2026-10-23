from model_client import ANTHROPIC_API_URL, ANTHROPIC_API_KEY
from model_models import ModelRequest, ModelResponse


def extract_json(text):
    headers = {
        "Authorization": f"Bearer {ANTHROPIC_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": f"Extract structured JSON from the following text: {text}",
        "max_tokens_to_sample": 100,
    }
    response = requests.post(ANTHROPIC_API_URL, headers=headers, json=data)
    return ModelResponse(response.json()["completion"])
