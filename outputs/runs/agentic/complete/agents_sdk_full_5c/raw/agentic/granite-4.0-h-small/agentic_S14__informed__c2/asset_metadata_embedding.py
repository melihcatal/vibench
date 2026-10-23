import os
from storage_models import OCRResult, TranslationResult, MetadataEmbeddingResult, TextEmbeddingResult
from google.cloud import genai

def embed_metadata_and_text(ocr_result: OCRResult, translation_result: TranslationResult):
    """Embed object metadata (rich text) using Gemini Embeddings API.

    Returns a TextEmbeddingResult containing the combined raw string and its embedding vector.
    """
    # Build a rich metadata string
    metadata_str = (
        f"File: {ocr_result.key}\n"
        f"Detected language: {ocr_result.language}\n"
        f"Extracted text (first 500 chars): {ocr_result.text[:500]}...\n"
        f"Translated text (first 500 chars): {translation_result.translated_text[:500]}..."
    )
    # Initialize Gemini client using GOOGLE_API_KEY from env
    client = genai.Client()
    embed_model = client.embeddings.get_model("gemini-1.5-flash-embedding-2")
    response = embed_model.embed_content(metadata_str)
    embedding = response.data[0].embedding
    return TextEmbeddingResult(
        text=metadata_str,
        embedding=embedding
    )
