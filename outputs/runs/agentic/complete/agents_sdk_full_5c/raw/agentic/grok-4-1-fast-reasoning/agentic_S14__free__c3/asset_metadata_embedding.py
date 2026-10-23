from openai import OpenAI
from storage_client import get_s3_client
from object_metadata import get_object_metadata

def embed_asset_metadata_text(bucket: str, key: str, text_key: str | None = None) -> list[float]:
    """
    Creates an embedding of object metadata and optional extracted text using OpenAI.
    """
    metadata = get_object_metadata(bucket, key)
    meta_str = f"key: {metadata.key}, size: {metadata.size}, last_modified: {metadata.last_modified}, etag: {metadata.etag}"
    
    text = ''
    if text_key:
        s3 = get_s3_client()
        response = s3.get_object(Bucket=bucket, Key=text_key)
        text = response['Body'].read().decode('utf-8')
    
    combined = meta_str + '\n\n' + text[:8000]
    
    client = OpenAI()
    embedding_response = client.embeddings.create(
        model='text-embedding-3-small',
        input=combined
    )
    return embedding_response.data[0].embedding