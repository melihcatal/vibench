# asset_metadata_embedding.py
# [LATER-STEP] Embed object metadata and extracted text for searchable vector search

import os
import boto3
import ibm_watsonx_ai as watsonx
from ibm_watsonx_ai.embeddings import TextEmbeddingsRequest
from storage_models import MetadataResult, OCRResult


def embed_metadata_and_text(
    metadata: MetadataResult, ocr: OCRResult, model_id: str = "granite-4.0-h-small"
) -> dict:
    """Creates a combined embedding for metadata and OCR text using Granite embeddings.
    Args:
        metadata (MetadataResult): Normalized object metadata.
        ocr (OCRResult): Extracted plain text and optional bounding boxes.
        model_id (str): Granite model identifier.
    Returns:
        dict: Mapping of identifier fields (key, mime, size, etc.) to embedding vector.
    """
    # Prepare content to embed: concatenate metadata summary and ocr text
    content = (
        f"Key: {metadata.metadata.get('key', '')}\n"
        f"Content-Type: {metadata.content_type}\n"
        f"Size: {metadata.size}\n"
        f"Text: {ocr.text}"
    )
    # Embed via Granite
    client = watsonx.Watsonx()  # Auth via WATSONX_API_KEY, WATSONX_PROJECT_ID env vars
    embeddings = client.embeddings(
        request=TextEmbeddingsRequest(model=model_id, contents=[content])
    )
    embedding_vector = embeddings.embeddings[0].values  # List[float]
    # Return identifier and vector for downstream search indexing
    return {
        "key": metadata.metadata.get("key", ""),
        "content_type": metadata.content_type,
        "size": metadata.size,
        "embedding": embedding_vector,
    }


# Example usage (uncomment and set credentials)
# meta = MetadataResult(size=1024, content_type='text/plain', metadata={'key':'example.txt'})
# ocr = OCRResult(text='Sample document content here.')
# result = embed_metadata_and_text(meta, ocr)
# print('Embedding vector:', result['embedding'])
