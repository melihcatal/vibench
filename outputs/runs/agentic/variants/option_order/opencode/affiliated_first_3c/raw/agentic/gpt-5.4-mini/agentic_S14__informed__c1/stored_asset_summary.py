from typing import Optional

from openai import OpenAI


def stored_asset_summary(text: str, model: str = 'gpt-4.1-mini', api_key: Optional[str] = None) -> str:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'system', 'content': 'Summarize extracted asset content concisely.'},
            {'role': 'user', 'content': text},
        ],
    )
    return response.choices[0].message.content or ''
