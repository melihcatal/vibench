from typing import Dict, List, Optional
import os
from google.cloud import aiplatform
from sentence_transformers import SentenceTransformer
from document_client import get_document_client
from document_models import OCRResponse, LayoutResponse


def embed_text(text: str, model_name: str = "textembedding-gecko") -> List[float]:
    """Embed extracted document sections using Google Cloud Vertex AI Text Embedding."""
    aiplatform.init(
        project=os.getenv("GOOGLE_CLOUD_PROJECT_ID"), location="us-central1"
    )

    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    embeddings = model.get_embeddings([text])
    return embeddings[0].values


def embed_document_sections(image_path: str) -> Dict[str, List[float]]:
    """Embed extracted document sections for semantic retrieval."""
    from extract_text import extract_text
    from extract_layout import extract_layout

    ocr_result = extract_text(image_path)
    layout_result = extract_layout(image_path)

    embeddings = {
        "full_text": embed_text(ocr_result.text),
        "blocks": [embed_text(block.text) for block in layout_result.blocks],
        "paragraphs": [
            embed_text(paragraph.text) for paragraph in layout_result.paragraphs
        ],
    }

    return embeddings


def ocr_embedding(image_path: str) -> Dict[str, List[List[float]]]:
    """Embed extracted document sections for semantic retrieval."""
    embeddings = embed_document_sections(image_path)
    return {
        "full_text": [embeddings["full_text"]],
        "blocks": embeddings["blocks"],
        "paragraphs": embeddings["paragraphs"],
    }
