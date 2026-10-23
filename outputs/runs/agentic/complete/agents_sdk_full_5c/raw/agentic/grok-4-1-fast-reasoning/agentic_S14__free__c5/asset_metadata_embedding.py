import os
from openai import OpenAI
from storage_client import get_s3_client, download_object
from typing import Optional, List

def asset_metadata_embedding(
    bucket: str,
    key: str,
    model: str = 'text-embedding-3-small',
    region: Optional[str] = None
) -> List[float]:
    s3_client = get_s3_client(region)
    head_resp = s3_client.head_object(Bucket=bucket, Key=key)
    metadata_str = str(head_resp.get('Metadata', {}))
    content_bytes = download_object(s3_client, bucket, key)
    content_str = content_bytes.decode('utf-8', errors='ignore')
    combined_text = f'Metadata: {metadata_str}\nContent: {content_str}'
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=combined_text,
        model=model
    )
    return [float(x) for x in response.data[0].embedding]
