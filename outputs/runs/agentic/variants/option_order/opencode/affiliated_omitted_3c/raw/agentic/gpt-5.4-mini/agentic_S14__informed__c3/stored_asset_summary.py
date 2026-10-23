from typing import Optional

from mistralai import Mistral

from storage_client import get_bucket_name


def summarize_stored_asset(text: str, model: str = 'mistral-large-latest', max_tokens: int = 256) -> str:
    client = Mistral()
    response = client.chat.complete(model=model, messages=[{'role': 'user', 'content': text}], max_tokens=max_tokens)
    return response.choices[0].message.content
