import os
import json
from google.cloud import storage
from google.cloud import language_v1 as language
from google.cloud import translate_v2 as translate
from typing import Dict, Any
from storage_client import get_storage_client

def embed_metadata_and_text(bucket_name: str, object_name: str) -> Dict[str, Any]:
    """Combine object metadata, extracted text, translated text, and an embedding vector for search.

    Args:
        bucket_name (str): Bucket containing the object.
        object_name (str): Blob name of the object.

    Returns:
        Dict[str, Any]: JSON-serializable dictionary with fields:
            - metadata (dict): raw GCS metadata.
            - extracted_text (str): raw OCR text.
            - translated_text (str): text translated to English.
            - embedding (list[float]): vector embedding for the translated text.
    """
    client = get_storage_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(object_name)
    metadata = blob.metadata or {}
    # Grab plain text (e.g., OCR result) from metadata; if missing, try to extract it via Document AI
    extracted_text = metadata.get('extracted_text')
    if not extracted_text:
        # Simple fallback: download and use first 1000 chars (real pipelines would OCR)
        content = blob.download_as_bytes()
        extracted_text = content.decode('utf-8', errors='replace')[:1000]
        # Store for future reuse
        metadata['extracted_text'] = extracted_text
        blob.metadata = metadata
        blob.patch()
    
    # Translate to English for search
    translated = translate_text(extracted_text, target_lang='en')
    if not translated:
        translated = extracted_text
    
    # Get embedding via Google Cloud Natural Language (embeddings feature)
    client_lang = language.LanguageServiceClient()
    document = language.Document(content=translated, type_=language.Document.Type.PLAIN_TEXT)
    request = language.EmbedTextRequest(document=document, encoding_type='UTF8')
    response = client_lang.embed_content(request=request)
    embedding = list(response.embedding.values)
    
    combined = {
        'metadata': metadata,
        'extracted_text': extracted_text,
        'translated_text': translated,
        'embedding': embedding
    }
    return combined

# Helper to persist the enriched object back to GCS as JSON sidecar

def store_asset_embedding(bucket_name: str, object_name: str):
    enriched = embed_metadata_and_text(bucket_name, object_name)
    sidecar_name = f'{object_name}.embedding.json'
    bucket = get_storage_client().bucket(bucket_name)
    blob = bucket.blob(sidecar_name)
    blob.upload_from_string(json.dumps(enriched, ensure_ascii=False))
    print(f'Sidecar saved: gs://{bucket_name}/{sidecar_name}')
