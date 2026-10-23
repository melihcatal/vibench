from model_client import get_model_client
from model_models import ModelRequest, ModelResponse
from typing import Tuple

def collect_model_response(prompt: str) -> Tuple[str, dict]:
    client = get_model_client()
    request = ModelRequest(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": prompt}]
    )
    response = client.chat.completions.create(**request.dict())
    metadata = {
        "model": response.model,
        "usage": response.usage.dict(),
        "system_fingerprint": response.system_fingerprint
    }
    return response.choices[0].message.content, metadata