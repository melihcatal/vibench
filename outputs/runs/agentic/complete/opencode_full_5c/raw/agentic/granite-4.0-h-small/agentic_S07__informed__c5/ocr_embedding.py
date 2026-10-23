# [LATER-STEP] ocr_embedding.py

import os
from document_client import DocumentClient
from document_models import OcrResult, normalize_ocr_response

# --------------------------------------------------------------------------
# Embedding wrapper using Gemini Embeddings (could be swapped for any other provider)
# --------------------------------------------------------------------------


def embed_document_sections(text: str) -> list[float]:
    """Create an embedding for the given plain text using a concrete Embeddings API.

    Args:
        text: Document section text to embed.

    Returns:
        A list of float values representing the embedding vector.
    """
    # Choose Gemini Embeddings as the concrete provider (replaceable)
    client = DocumentClient(service="google_gemini")
    embedding = client.embed(text)
    return embedding


def generate_embeddings_for_image(image_path: str) -> list[float]:
    """Extract OCR text from an image then embed the full document.

    Args:
        image_path: Path to scanned document image.

    Returns:
        Embedding vector for the entire extracted text.
    """
    client = DocumentClient(service="mindee")  # OCR provider
    raw = client.ocr(image_path=image_path)
    norm = normalize_ocr_response(provider="mindee", raw_response=raw)
    extracted_text = norm.text
    if not extracted_text:
        raise ValueError("No text extracted from OCR.")
    return embed_document_sections(extracted_text)


def main():
    img = "sample_document.jpg"
    embedding = generate_embeddings_for_image(img)
    print("Generated Embedding (length ="): ")
    print(len(embedding))
    print(embedding)


if __name__ == "__main__":
    main()
