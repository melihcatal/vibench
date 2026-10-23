from openai import OpenAI
from storage_client import get_s3_client

def summarize_stored_asset(bucket: str, key: str) -> str:
    """
    Summarizes text content from a stored asset using OpenAI GPT.
    """
    s3 = get_s3_client()
    response = s3.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    
    client = OpenAI()
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': f'Summarize the following content:\n\n{content[:8000]}'}]
    )
    return completion.choices[0].message.content