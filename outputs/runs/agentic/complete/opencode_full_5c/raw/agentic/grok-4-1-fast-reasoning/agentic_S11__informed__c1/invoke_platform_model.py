from model_client import get_client
from typing import List, Dict


def invoke_platform_model(messages: List[Dict[str, str]], deployment_id: str) -> str:
    client = get_client()
    response = client.chat.completions.create(
        model=deployment_id,
        messages=messages,
        max_tokens=1000,
    )
    return response.choices[0].message.content
