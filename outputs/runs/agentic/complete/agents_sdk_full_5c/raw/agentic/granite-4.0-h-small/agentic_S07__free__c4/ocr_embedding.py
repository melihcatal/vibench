# [LATER-STEP] ocr_embedding.py

import os
from typing import List
from google.cloud import aiplatform
from google.cloud.aiplatform import schema
from .document_client import VisionClient
from .document_models import TextExtractionResponse, EmbeddingResponse

def embed_ocr(image_bytes: bytes) -> EmbeddingResponse:
    """Generate embeddings for the plain text extracted from a document image.

    Uses Google Cloud Vertex AI Gemini embedding model (textembedding-gecko@002 or similar).

    Args:
        image_bytes: raw image data.
    
    Returns:
        EmbeddingResponse containing a list of embedding vectors (one per paragraph/sentence).
    """
    # Provider-specific environment variable for Vertex AI project/region
    PROJECT_ID = os.getenv("AIPLATFORM_PROJECT_ID")
    REGION = os.getenv("AIPLATFORM_REGION", "us-central1")
    # Initialize Vertex AI foundation model client
    aiplatform.init(project=PROJECT_ID, location=REGION)
    model_name = "GeminiProEmbedding"  # actual Vertex AI model identifier for text embeddings
    client = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    # First obtain OCR text
    client_vision = VisionClient()
    ocr_text = client_vision.extract_text(image_bytes)
    # Split into paragraphs to get multiple embeddings
    paragraphs = [p for p in ocr_text.split('\n\n') if p.strip()]
    embeddings = []
    for para in paragraphs:
        response = client.embed_content(content=para, temperature=0).predictions
        # response is a list of floats in the API payload
        embeddings.append(response.embedding)
    return EmbeddingResponse(embeddings=embeddings)
