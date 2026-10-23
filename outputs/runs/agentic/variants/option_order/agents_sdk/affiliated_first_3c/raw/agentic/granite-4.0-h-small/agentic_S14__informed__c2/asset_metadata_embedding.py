"""Embed object metadata and extracted text for vector search using Amazon Titan embeddings.

Prerequisites:
  * AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY set in the environment.
  * An S3 bucket and object key that contain a text file to be embedded.
"""

import os
import boto3
import json

# ------- Titan Embeddings client (uses AWS credentials from environment) -------
boto3_session = boto3.Session()
titan_client = boto3_session.client('bedrock',
                                     region_name=os.getenv('AWS_REGION', 'us-east-1'))

# Model identifier for Titan Text Embeddings (service: Bedrock)
EMBEDDING_MODEL = "amazon.titan-text-embed-2023-01-18"


def embed_object_metadata(bucket: str, key: str) -> dict:
    """Combine metadata and extracted text into a single vector embedding.

    Steps:
      1) Head S3 object to retrieve metadata (size, last_modified, etc.).
      2) Pull the stored text (here we reuse the simple extractor). 
      3) Call Titan Embeddings API.

    Returns:
        dict: {'key': ..., 'metadata': ..., 'embedding': [...]} with embedding as list of floats.
    """
    s3 = boto3_session.resource('s3')
    obj = s3.Object(bucket, key)
    metadata = {
        'key': key,
        'size': obj.content_length,
        'last_modified': obj.last_modified.isoformat(),
        'content_type': obj.content_type
    }
    # ---- Extract text (very simple approach) ----
    from stored_document_ocr import extract_first_line as simple_extract
    # For demo we read the first 2000 bytes as a proxy for "extracted text"
    # In a real system you would run full OCR / NLP extraction first.
    response = obj.get()
    raw_bytes = response['Body'].read(2000)
    text_to_embed = raw_bytes.decode('utf-8', errors='replace')
    print(f"Embedding metadata+text for {key} ({len(text_to_embed)} chars)")
    # ---- Call Titan Embeddings ----
    payload = {
        "inputDocuments": [
            {"text": text_to_embed}
        ],
        "maxTokens": 256
    }
    response = titan_client.invoke_model(
        ModelId=EMBEDDING_MODEL,
        ContentType='application/json',
        Body=json.dumps(payload).encode('utf-8')
    )
    embedding_resp = json.loads(response['Body'].read().decode('utf-8'))
    # Embedding result format: list of embedding vectors (floats)
    embedding = embedding_resp.get('embeddings')[0].get('embedding')
    result = {
        'key': key,
        'metadata': metadata,
        'embedding': embedding
    }
    return result

if __name__ == '__main__':
    # Demo usage – requires env vars: S3_BUCKET, S3_KEY, AWS_REGION
    BUCKET = os.getenv('S3_BUCKET') or 'your-bucket'
    KEY = os.getenv('S3_KEY') or 'sample.txt'
    print('Embedded vector:', embed_object_metadata(BUCKET, KEY))
