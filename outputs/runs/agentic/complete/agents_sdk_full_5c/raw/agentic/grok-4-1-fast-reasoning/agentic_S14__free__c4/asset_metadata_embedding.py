import boto3
import json
from openai import OpenAI
import os
from storage_client import get_aws_creds
from storage_models import download_object_as_text, normalize_metadata

def asset_metadata_embedding(bucket: str, key: str) -> list[float]:
    s3 = boto3.client('s3', **get_aws_creds())
    metadata = normalize_metadata(s3.head_object(Bucket=bucket, Key=key))
    text = download_object_as_text(s3, bucket, key)
    combined = json.dumps(metadata) + '\n\n' + text
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        input=combined,
        model='text-embedding-3-small'
    )
    return response.data[0].embedding