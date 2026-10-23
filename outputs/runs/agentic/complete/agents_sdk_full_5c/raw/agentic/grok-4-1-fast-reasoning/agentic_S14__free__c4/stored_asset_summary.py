import boto3
from openai import OpenAI
import os
from storage_client import get_aws_creds
from storage_models import download_object_as_text

def stored_asset_summary(bucket: str, key: str) -> str:
    s3 = boto3.client('s3', **get_aws_creds())
    text = download_object_as_text(s3, bucket, key)
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': f'Provide a concise summary of the following content:\n\n{text}'}]
    )
    return response.choices[0].message.content