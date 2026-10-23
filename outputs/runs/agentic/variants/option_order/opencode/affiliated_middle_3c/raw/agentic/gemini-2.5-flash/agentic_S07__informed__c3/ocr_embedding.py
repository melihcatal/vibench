import os
import google.generativeai as genai
from document_models import OCREmbeddingRequest, OCREmbeddingResult


def embed_ocr_sections(request: OCREmbeddingRequest) -> OCREmbeddingResult:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=api_key)

    model = "models/embedding-001"

    embeddings = []
    for text_chunk in request.text_sections:
        response = genai.embed_content(model=model, content=text_chunk)
        embeddings.append(response["embedding"])

    return OCREmbeddingResult(embeddings=embeddings)
