from typing import Dict, Any
from model_client import ModelClient


def extract_json(
    text: str, schema: Dict[str, Any], max_tokens: int = 500, temperature: float = 0.2
) -> Dict[str, Any]:
    client = ModelClient()
    return client.extract_json(text, schema, max_tokens, temperature)
