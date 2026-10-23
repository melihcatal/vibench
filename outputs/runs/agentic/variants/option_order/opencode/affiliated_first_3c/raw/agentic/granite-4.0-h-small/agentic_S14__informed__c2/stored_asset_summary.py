import os
import json
from storage_client import StorageClient
from storage_models import StorageModels
from google.cloud import genai
from google.cloud import storage as google_storage

# Use Google Gemini API for LLM inference on extracted content
# Authenticate via GOOGLE_APPLICATION_CREDENTIALS environment variable

# Set the model you want to use (e.g., gemini-pro for chat)
MODEL = 'gemini-pro'

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def stored_asset_summary(object_key: str, bucket: str = 'your-bucket-name') -> str:
    """Summarize content extracted from a stored asset using Gemini LLM.",
    storage = google_storage.Client()
    blob = storage.bucket(bucket).get_blob(object_key)
    if not blob:
        raise FileNotFoundError(f'Object {object_key} not found in bucket {bucket}')
    content = blob.download_as_text()

    # Build a prompt for Gemini; simple summarization request
    prompt = f"Summarize the following document in three bullet points:\n\n{content}"
    # Call Gemini chat endpoint
    response = genai.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    # Return the Gemini generated summary
    return response.candidates[0].content.parts[0].text.strip()

# Example usage (uncomment to test)
# print(stored_asset_summary('assets/report.pdf'))
