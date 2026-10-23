import os
import datetime
from storage_client import get_managed_storage_client
from google.cloud import generativeai as genai
from google.cloud import aiplatform


def embed_asset_metadata(bucket_name, object_key):
    """Embed object metadata and extracted text for search using Gemini embeddings.

    Returns an embedding vector (list of floats).
    """
    # Configure LLM client
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")
    # Define the metadata (example)
    metadata = {
        "bucket": bucket_name,
        "object_key": object_key,
        "size_bytes": 1024,
        "mime_type": "text/plain",
    }
    # Placeholder: retrieve actual extracted text from previous OCR step
    extracted_text = "Sample text from the stored document that needs embedding."
    # Combine metadata and text into a prompt for embedding
    prompt = f"Embed the following metadata and text for semantic search:\\nMetadata: {metadata}\\nText: {extracted_text}"
    # Use Gemini to produce an embedding (uses Gemini embeddings endpoint under the hood)
    embedding = genai.embed_contents(prompt, model="gemini-1.5-flash")
    return embedding.embedding
