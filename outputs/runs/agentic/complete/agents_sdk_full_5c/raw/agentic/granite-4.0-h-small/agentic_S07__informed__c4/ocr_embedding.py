import os
from google.cloud import genai

gemini_api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=gemini_api_key)

def embed_document_sections(ocr_text, model="gemini-1.5-flash-001"):
    embeddings = client.embed_content(model=model, text=ocr_text)
    return embeddings.get("embeddings")
