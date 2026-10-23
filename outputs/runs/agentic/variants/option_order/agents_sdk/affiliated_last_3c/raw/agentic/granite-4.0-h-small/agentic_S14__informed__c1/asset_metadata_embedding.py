import os
import boto3
import openai
from storage_client import get_s3_client
from storage_models import normalize_head_params

def embed_asset_metadata(bucket, key):
    """Creates an embedding for the combined metadata and plain text of an S3 object.
    Uses Amazon Titan Text Embeddings via Bedrock Runtime.
    Returns a list of floats representing the embedding vector.
    """
    # Get S3 client (not used for embedding but for demo download of text)
    s3 = get_s3_client()
    # Download plain text (assume UTF-8 encoding)
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp_file:
        s3.download_file(bucket, key, tmp_file.name)
        print(f'Downloaded {key} for embedding.')
        content = open(tmp_file.name, 'r', encoding='utf-8').read()
        os.unlink(tmp_file.name)
    # Prepare metadata (simple example)
    metadata = {
        'bucket': bucket,
        'key': key,
        'size_bytes': None  # could use head_object if needed
    }
    combined = f"Metadata: {metadata}\nContent: {content}"
    # Call Titan Embeddings via Bedrock Runtime
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    embedding_response = client.create_embedding(
        ModelId='amazon.titan-embedding-text-v1',
        Input={'text': combined}
    )
    embedding = embedding_response['Embedding']  # list of floats
    print(f'Embedding vector length: {len(embedding)}')
    return embedding
