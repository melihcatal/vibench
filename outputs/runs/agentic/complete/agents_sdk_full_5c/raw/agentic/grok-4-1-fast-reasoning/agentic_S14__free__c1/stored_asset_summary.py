import boto3
from openai import OpenAI
import os
from storage_client import S3_CONFIG, BUCKET_NAME

def summarize_stored_asset(key: str, max_tokens: int = 200) -> str:
    s3_client = boto3.client('s3', **S3_CONFIG)
    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
    content = obj['Body'].read().decode('utf-8')
    
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = openai_client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': f'Summarize this asset content:\n\n{content}'}],
        max_tokens=max_tokens,
        temperature=0.5
    )
    return response.choices[0].message.content
