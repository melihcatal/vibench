import boto3
from openai import OpenAI
import os
from storage_client import S3_CONFIG, BUCKET_NAME
from object_metadata import get_object_metadata

def embed_asset_metadata_and_text(key: str) -> list[float]:
    s3_client = boto3.client('s3', **S3_CONFIG)
    obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=key)
    text = obj['Body'].read().decode('utf-8')[:4000]  # truncate for embedding
    
    metadata = get_object_metadata(key)
    combined_text = f"Metadata: {metadata.model_dump()}\nContent: {text}"
    
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = openai_client.embeddings.create(
        model='text-embedding-3-small',
        input=combined_text
    )
    return response.data[0].embedding
