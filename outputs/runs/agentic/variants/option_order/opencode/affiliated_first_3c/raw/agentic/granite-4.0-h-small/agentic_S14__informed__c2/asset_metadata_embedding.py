import os
import json
from storage_client import StorageClient
from storage_models import StorageModels
from google.cloud import genai
from google.cloud import storage as google_storage

# Use Google Gemini API for embeddings on metadata and extracted text
# Authenticate via GOOGLE_APPLICATION_CREDENTIALS environment variable

MODEL = 'gemini-pro'
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def asset_metadata_embedding(object_key: str, bucket: str = 'your-bucket-name') -> list[float]:
    """Embed metadata (e.g., JSON metadata stored alongside the asset) using Gemini embeddings.",
    storage = google_storage.Client()
    blob = storage.bucket(bucket).get_blob(object_key)
    if not blob:
        raise FileNotFoundError(f'Object {object_key} not found in bucket {bucket}')
    # Assume metadata is stored as JSON in the same key with a .meta suffix
    meta_blob = storage.bucket(bucket).get_blob(f'{object_key}.meta')
    metadata_text = meta_blob.download_as_text() if meta_blob else ''

    # Build embedding prompt for Gemini
    prompt = f"Create a 1536‑dimensional embedding for the following metadata:\n\n{metadata_text}"
    response = genai.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    # Gemini returns a list of embedding vectors; we take the first as the result
    embedding = response.candidates[0].content.parts[0].text.strip()
    return json.loads(embedding)

# Example usage (uncomment to test)
# print(asset_metadata_embedding('assets/report.pdf'))
