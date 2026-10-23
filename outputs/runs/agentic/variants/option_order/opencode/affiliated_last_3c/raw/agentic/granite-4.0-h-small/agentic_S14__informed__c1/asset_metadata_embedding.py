import os
import json
import boto3
from google.cloud import generativeai as genai
from google.cloud import translate_v2 as translate
from google.cloud import documentai_v1 as documentai
from storage_client import ManagedStorageClient


def embed_asset_metadata(bucket_name: str, object_key: str) -> dict:
    """Embed metadata and extracted text from a stored asset for search indexing using Gemini embeddings.

    The function gathers metadata via S3 HEAD, extracts text via Google Document AI, translates if needed,
    concatenates data, and then queries the Gemini embeddings API to obtain an embedding vector.
    """
    # ---------- 1. Retrieve basic metadata from S3 ----------
    s3 = ManagedStorageClient.get_s3_client()
    try:
        meta = s3.head_object(Bucket=bucket_name, Key=object_key)
    except Exception as e:
        raise RuntimeError(f"Failed to fetch metadata: {e}")
    metadata = {
        "bucket": bucket_name,
        "key": object_key,
        "last_modified": meta["LastModified"].isoformat(),
        "size_bytes": meta["ContentLength"],
        "storage_class": meta["StorageClass"],
    }

    # ---------- 2. Extract text using Document AI ----------
    # Assumes you have set up a Document AI processor and exported its URI env var
    processor_uri = os.getenv("DOCUMENT_AI_PROCESSOR_URI")
    if not processor_uri:
        raise RuntimeError("DOCUMENT_AI_PROCESSOR_URI environment variable not set")
    client_service = documentai.DocumentProcessorServiceClient()
    # Stream document from S3 directly to avoid local file writes
    resp = client_service.process_document(
        request={
            "name": processor_uri,
            "document": {
                "content": s3.get_object(Bucket=bucket_name, Key=object_key)[
                    "Body"
                ].read(),
                "mime_type": "application/pdf",  # adjust for actual mime type
            },
        }
    )
    # Simple extraction of full text (first page) for demo
    full_text = ""
    if resp.document.pages:
        full_text = resp.document.pages[0].layout[0].text or ""

    # Optional: translate text to English for consistent embeddings (requires Google credentials)
    try:
        translator = translate.Client()
        translated = translator.translate(full_text, target_language="en")
        text = translated["translatedText"]
    except Exception:
        text = full_text  # fallback to untranslated text

    # ---------- 3. Generate embedding with Gemini ----------
    genai.configure(
        api_key=os.getenv("GEMINI_API_KEY"), project=os.getenv("GEMINI_PROJECT_ID")
    )
    model = genai.GenerativeModel("gemini-1.5-flash")  # example model ID
    embedding_request = {
        "contents": [
            {
                "text": f"Metadata: {json.dumps(metadata)}\\n\\nDocument excerpt: {text[:2000]}"
            }
        ],
        "parameters": {
            "temperature": 0,
            "model": "gemini-1.5-flash-embedding",  # embedding-specific model ID
        },
    }
    response = model.embed_content(embedding_request)
    embedding_vector = response.embeddings[0].embedding  # list of floats
    return {
        "metadata": metadata,
        "embedding": embedding_vector,
    }
