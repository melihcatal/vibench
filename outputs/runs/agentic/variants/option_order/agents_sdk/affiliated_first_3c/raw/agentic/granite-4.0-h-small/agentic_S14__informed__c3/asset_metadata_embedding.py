import os
import json
import boto3
from google.cloud import genai
from google.cloud import translate_v2 as translate
from storage_models import ObjectMetadata

# Load Gemini model (Gemini Pro) from Vertex AI
# Ensure GOOGLE_APPLICATION_CREDENTIALS points to your credentials

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
embedder = genai.Service.from_pretrained('textembedding-gecko')  # Gemini embeddings

translate_client = translate.Client()


def embed_object_metadata_and_text(bucket_name: str, object_key: str) -> dict:
    """
    Embed object metadata and extracted OCR text into a high‑dimensional vector using Gemini embeddings.
    Returns a dict containing:
        - object metadata
        - raw extracted text
        - the numeric embedding vector
    """
    # Get S3 object metadata
    s3 = boto3.client('s3')
    meta = s3.head_object(Bucket=bucket_name, Key=object_key)
    meta_dict: ObjectMetadata = {
        'Key': meta['Key'],
        'Size': meta['ContentLength'],
        'StorageClass': meta['StorageClass'],
        'LastModified': meta['LastModified'].isoformat() if isinstance(meta['LastModified'], (datetime.datetime)) else str(meta['LastModified']),
        'ETag': meta['ETag'],
        'Metadata': meta.get('Metadata', {})
    }
    # Extract text via OCR (document_ocr function from stored_document_ocr)
    from stored_document_ocr import ocr_stored_document
    text = ocr_stored_document(bucket_name, object_key)
    # Translate text if needed (optional)
    target = os.getenv('TRANSLATE_TARGET_LANGUAGE', 'en')
    if target and target.lower() != 'en':
        result = translate_client.translate(text, target_language=target)
        text = result['translatedText']
    # Generate embedding with Gemini
    embedding_response = embedder.embed_content(text=text)
    embedding_vector = embedding_response['embedding']  # list of floats
    # Assemble final payload
    payload = {
        'metadata': meta_dict,
        'text': text,
        'embedding': embedding_vector
    }
    return payload
