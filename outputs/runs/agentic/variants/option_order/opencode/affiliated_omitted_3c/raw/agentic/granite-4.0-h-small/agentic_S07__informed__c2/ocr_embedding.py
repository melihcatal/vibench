import os
import json
import requests
import hashlib
from gensim.models import KeyedVectors

# Utility imports
from document_client import DocumentClient
from document_models import chunk_text

# Embedding model chosen: OpenAI embeddings (via OpenAI API) for demonstration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = "https://api.openai.com/v1/embeddings"


def embed_document_sections(
    file_path: str, model: str = "text-embedding-ada-002"
) -> dict:
    """
    Break the extracted document text into semantic sections (paragraphs) and embed each using OpenAI.
    Returns a mapping from a section hash to its embedding vector.
    """
    # Step 1: Get text content using OCR helper (here we reuse the OCR client but only for text extraction)
    client = DocumentClient(service="documentai")
    with open(file_path, "rb") as img:
        img_bytes = img.read()
    text = client.extract_text(img_bytes)
    # Chunk into paragraphs
    paragraphs = chunk_text(text, size=500)  # ~500 token chunks

    embeddings = {}
    for idx, para in enumerate(paragraphs):
        payload = {"model": model, "input": para}
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        resp = requests.post(OPENAI_ENDPOINT, json=payload, headers=headers)
        resp.raise_for_status()
        vec = resp.json()["data"][0]["embedding"]
        section_hash = hashlib.sha256(para.encode()).hexdigest()
        embeddings[section_hash] = vec
    return embeddings
