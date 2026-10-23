import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from google.cloud import aiplatform
from document_models import NormalizedDocument, LayoutElement


def embed_document_sections(
    normalized_doc: NormalizedDocument, section_type: str = "paragraph"
) -> List[Dict[str, Any]]:
    """Embed extracted document sections for semantic retrieval using Google Vertex AI."""

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")

    # Initialize Vertex AI
    aiplatform.init(project=project_id, location=location)

    # Get text sections based on type
    sections = get_sections_by_type(normalized_doc, section_type)

    if not sections:
        return []

    # Prepare texts for embedding
    texts = [section["text"] for section in sections if section["text"].strip()]

    if not texts:
        return []

    # Create embeddings using Vertex AI Text Embedding model
    from google.cloud.aiplatform_v1.types import PredictResponse
    from google.cloud.aiplatform_v1.services.prediction_service import (
        PredictionServiceClient,
    )

    client = PredictionServiceClient()

    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/textembedding-gecko@001"

    instances = [{"content": text} for text in texts]

    response = client.predict(endpoint=endpoint, instances=instances)

    embeddings = []
    for i, prediction in enumerate(response.predictions):
        if i < len(sections):
            section = sections[i]
            embedding_vector = prediction.get("embeddings", {}).get("values", [])

            embeddings.append(
                {
                    "text": section["text"],
                    "embedding": embedding_vector,
                    "section_type": section["type"],
                    "section_index": section.get("index", i),
                    "confidence": section.get("confidence", 0.0),
                    "provider": "google_vertex_ai",
                    "model": "textembedding-gecko@001",
                    "embedding_dimension": len(embedding_vector),
                }
            )

    return embeddings


def get_sections_by_type(
    normalized_doc: NormalizedDocument, section_type: str
) -> List[Dict[str, Any]]:
    """Get document sections based on type (paragraph, block, line, etc.)."""

    sections = []

    if section_type == "paragraph" and normalized_doc.text:
        # Split text into paragraphs
        paragraphs = normalized_doc.text.split("\n\n")
        for i, para in enumerate(paragraphs):
            if para.strip():
                sections.append(
                    {
                        "text": para.strip(),
                        "type": "paragraph",
                        "index": i,
                        "confidence": 1.0,
                    }
                )

    elif section_type == "block" and normalized_doc.layout_elements:
        # Use layout blocks
        for i, elem in enumerate(normalized_doc.layout_elements):
            if elem.type == "block" and elem.text.strip():
                sections.append(
                    {
                        "text": elem.text,
                        "type": "block",
                        "index": i,
                        "confidence": elem.confidence,
                        "bounding_box": elem.bounding_box,
                    }
                )

    elif section_type == "table" and normalized_doc.tables:
        # Use table content
        for table_idx, table in enumerate(normalized_doc.tables):
            table_text = ""
            for row_idx, row in enumerate(table.rows):
                row_text = " | ".join([cell.text for cell in row])
                table_text += f"Row {row_idx}: {row_text}\n"

            if table_text.strip():
                sections.append(
                    {
                        "text": table_text.strip(),
                        "type": "table",
                        "index": table_idx,
                        "confidence": 0.8,  # Default confidence for tables
                        "row_count": table.row_count,
                        "column_count": table.column_count,
                    }
                )

    elif section_type == "key_value" and normalized_doc.key_value_pairs:
        # Use key-value pairs
        for i, pair in enumerate(normalized_doc.key_value_pairs):
            pair_text = f"{pair.key}: {pair.value}"
            sections.append(
                {
                    "text": pair_text,
                    "type": "key_value",
                    "index": i,
                    "confidence": pair.confidence,
                    "key": pair.key,
                    "value": pair.value,
                }
            )

    return sections


def semantic_search(
    query: str, embeddings: List[Dict[str, Any]], top_k: int = 5
) -> List[Dict[str, Any]]:
    """Perform semantic search on embedded document sections."""

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us")

    # Embed the query
    aiplatform.init(project=project_id, location=location)

    from google.cloud.aiplatform_v1.services.prediction_service import (
        PredictionServiceClient,
    )

    client = PredictionServiceClient()
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/textembedding-gecko@001"

    query_response = client.predict(endpoint=endpoint, instances=[{"content": query}])

    if not query_response.predictions:
        return []

    query_embedding = (
        query_response.predictions[0].get("embeddings", {}).get("values", [])
    )

    # Calculate cosine similarities
    results = []
    for emb in embeddings:
        if "embedding" not in emb or not emb["embedding"]:
            continue

        similarity = cosine_similarity(query_embedding, emb["embedding"])

        results.append(
            {
                "text": emb["text"],
                "similarity": similarity,
                "section_type": emb["section_type"],
                "section_index": emb.get("section_index", 0),
                "confidence": emb.get("confidence", 0.0),
                "metadata": {
                    k: v
                    for k, v in emb.items()
                    if k not in ["text", "embedding", "similarity"]
                },
            }
        )

    # Sort by similarity and return top_k
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return results[:top_k]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0

    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = np.sqrt(sum(a * a for a in vec1))
    norm2 = np.sqrt(sum(b * b for b in vec2))

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def create_document_index(normalized_doc: NormalizedDocument) -> Dict[str, Any]:
    """Create a searchable index from document embeddings."""

    # Embed different section types
    paragraph_embeddings = embed_document_sections(normalized_doc, "paragraph")
    block_embeddings = embed_document_sections(normalized_doc, "block")
    table_embeddings = embed_document_sections(normalized_doc, "table")
    kv_embeddings = embed_document_sections(normalized_doc, "key_value")

    all_embeddings = (
        paragraph_embeddings + block_embeddings + table_embeddings + kv_embeddings
    )

    return {
        "document_id": normalized_doc.metadata.get("document_id", "unknown"),
        "embeddings": all_embeddings,
        "embedding_count": len(all_embeddings),
        "provider": "google_vertex_ai",
        "model": "textembedding-gecko@001",
        "created_at": datetime.now().isoformat(),
    }


def batch_embed_documents(documents: List[NormalizedDocument]) -> List[Dict[str, Any]]:
    """Batch embed multiple documents."""

    indices = []
    for doc in documents:
        index = create_document_index(doc)
        indices.append(index)

    return indices
