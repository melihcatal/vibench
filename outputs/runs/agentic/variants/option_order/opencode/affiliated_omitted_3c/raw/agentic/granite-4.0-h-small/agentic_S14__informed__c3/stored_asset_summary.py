# stored_asset_summary.py
import os
from google.cloud import generativeai as genai
from google.cloud import storage
from storage_client import get_client, bucket_name
from storage_models import normalize_object_name

# Configure Gemini as the LLM provider
SERVICE = "Google Gemini API"
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def summarize_asset(object_name: str, max_output_tokens: int = 500) -> str:
    """Generate a concise summary of the text extracted from a stored asset."""
    # Download the file contents
    client = get_client()
    bucket = client.bucket(bucket_name())
    blob = bucket.blob(normalize_object_name(object_name))
    text = blob.download_as_text()
    # Call Gemini for summarization
    response = model.generate_content(
        text,
        generation_config=genai.GenerativeModel.GenerationConfig(
            max_output_tokens=max_output_tokens, temperature=0.2
        ),
    )
    return response.text
