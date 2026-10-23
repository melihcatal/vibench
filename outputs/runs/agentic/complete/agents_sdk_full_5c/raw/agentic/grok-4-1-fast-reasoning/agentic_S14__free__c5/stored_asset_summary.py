import os
from openai import OpenAI
from storage_client import get_s3_client, download_object
from typing import Optional

def stored_asset_summary(
    bucket: str,
    key: str,
    model: str = 'gpt-3.5-turbo',
    region: Optional[str] = None
) -> str:
    s3_client = get_s3_client(region)
    content_bytes = download_object(s3_client, bucket, key)
    content = content_bytes.decode('utf-8')
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model=model,
        messages=[
            {'role': 'user', 'content': f'Provide a concise summary of the following content:\n\n{content}'}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content
