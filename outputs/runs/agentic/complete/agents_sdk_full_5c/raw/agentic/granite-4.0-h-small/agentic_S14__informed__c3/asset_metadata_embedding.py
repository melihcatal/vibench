import os
import boto3
from google.cloud import genai
from storage_models import ObjectMetadataResult
from typing import Dict

def embed_metadata(bucket_name: str, object_key: str) -> Dict[str, str]:
    """Embed object metadata and any extracted text for downstream search.

    Uses Google Gemini embeddings via the genai library. The credentials are taken from
    GOOGLE_API_KEY environment variable. The function first fetches object metadata via the
    S3 client and then creates an embedding of a JSON representation of that metadata.
    """
    # Get metadata using our helper S3 client
    client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    meta_resp = client.head_object(Bucket=bucket_name, Key=object_key)
    metadata = {
        'bucket': bucket_name,
        'key': object_key,
        'size': meta_resp.get('ContentLength'),
        'content_type': meta_resp.get('ContentType'),
        'last_modified': str(meta_resp.get('LastModified'))
    }
    metadata_json = str(metadata)  # convert to deterministic string representation
    # Create embedding via Gemini
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    model = genai.GeminiModel('gemini-1.5-flash')
    embedding = model.embed_content(metadata_json)
    # Return a dictionary that can be stored in a vector DB
    return {
        'object_id': f"s3://{bucket_name}/{object_key}",
        'embedding': embedding['embedding'],  # list of floats
        'metadata': metadata
    }
