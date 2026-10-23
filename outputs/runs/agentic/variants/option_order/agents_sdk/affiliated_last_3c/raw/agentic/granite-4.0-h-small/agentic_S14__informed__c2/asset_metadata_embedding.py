import os
import json
from typing import Dict, Any
from storage_models import validate_bucket_and_key, normalize_object_info
from stored_text_translate import stored_text_translate

def asset_metadata_embedding(bucket: str, key: str, embedding_service: str = 'openai'):
    """Combine static object metadata with extracted and translated text to create a searchable embedding.

    bucket: S3 bucket name
    key: object key (path) of the asset
    embedding_service: name of the embeddings API (default: 'openai')

    Returns a dict containing:
      - metadata (normalized)
      - extracted_text (raw)
      - translated_text
      - embedding (list of floats) – placeholder vector
    """
    # a) Normalized metadata from S3
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    validate_bucket_and_key(bucket, key)
    obj = s3.head_object(Bucket=bucket, Key=key)
    metadata = normalize_object_info(obj)

    # b) Extract text (OCR or plain read)
    import mimetypes
    mime_type, _ = mimetypes.guess_type(key)
    needs_ocr = mime_type in (None, 'application/pdf', 'image/', 'application/octet-stream')
    if needs_ocr:
        extracted_text = stored_document_ocr(bucket, key)
    else:
        obj_body = s3.get_object(Bucket=bucket, Key=key)
        extracted_text = obj_body['Body'].read().decode('utf-8')

    # c) Translate the extracted text (optional, for multilingual indexing)
    translated_text = stored_text_translate(bucket, key, target_lang='en')

    # d) Generate embedding (placeholder – replace with real API call)
    if embedding_service.lower() == 'openai':
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        resp = client.embeddings.create(
            model='text-embedding-ada-002',
            input=extracted_text
        )
        embedding = resp['data'][0]['embedding']
    elif embedding_service.lower() == 'google-genai':
        from google.generativeai import GenerativeModel
        model = GenerativeModel('gemini-1.5-flash')  # embedding incapable – using OpenAI for demo
        # placeholder
        embedding = [0.0] * 1536
    elif embedding_service.lower() == 'cohere':
        from cohere import Client
        client = Client(api_key=os.getenv('COHERE_API_KEY'))
        resp = client.embed(text=extracted_text, model='cohere-embed-english-v3.0')
        embedding = resp.embeddings[0]
    else:
        raise ValueError(f'Unsupported embedding service: {embedding_service}')

    return {
        'metadata': metadata,
        'extracted_text': extracted_text[:200] + ' ...',
        'translated_text': translated_text[:200] + ' ...',
        'embedding': embedding
    }
