import os
from google.cloud import storage
from google.cloud import documentai_v1 as documentai

def embed_metadata_and_text(bucket_name, blob_name, model_id=None):
    """Embed object metadata + extracted text using Google Gemini Embeddings.",
    # Assume metadata is stored in JSON in a sibling file named <blob_name>.meta.json
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    # Load metadata and text (for illustration we use placeholder) 
    metadata = {
        "filename": blob_name,
        "size": blob.size,
        "content_type": blob.content_type,
    }
    # Placeholder extracted text, replace with real OCR/LLM output in production
    extracted_text = "This is the content of the document stored in GCS."
    # Concatenate for embedding
    prompt = f"{extracted_text}\\nMetadata: {metadata}"
    # Embed using Gemini (requires GOOGLE_API_KEY env var)
    client_gemini = documentai.DocumentAIServiceClient()
    # Use the default model or override model_id if provided
    model = model_id if model_id else "gemini-1.5-flash"
    embeddings = client_gemini.embed_document(model=model, document=prompt)
    return {
        "embeddings": embeddings.embeddings,
        "metadata": metadata,
        "text_used": extracted_text
    }
