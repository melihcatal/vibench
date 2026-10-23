"""
[LATER-STEP] Embed extracted document sections for semantic retrieval.
Uses Google Cloud Vertex AI text embedding models to generate vector embeddings
for OCR-extracted document sections, enabling semantic search and retrieval.
"""

import os
from typing import Optional, List, Dict, Any
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel

from document_client import GOOGLE_CLOUD_PROJECT


GOOGLE_CLOUD_VERTEX_AI_ENDPOINT = "aiplatform.googleapis.com"
GOOGLE_CLOUD_EMBEDDING_MODEL = "textembedding-gecko@003"
GOOGLE_CLOUD_LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")


class VertexAIEmbeddingClient:
    """Client wrapper for Google Cloud Vertex AI Text Embedding API."""

    def __init__(
        self,
        project: Optional[str] = None,
        location: Optional[str] = None,
        credentials_path: Optional[str] = None,
    ):
        self.project = project or GOOGLE_CLOUD_PROJECT
        self.location = location or GOOGLE_CLOUD_LOCATION
        self.model_name = GOOGLE_CLOUD_EMBEDDING_MODEL

        aiplatform.init(
            project=self.project,
            location=self.location,
        )

        self.embedding_model = TextEmbeddingModel.from_pretrained(self.model_name)

    def get_embedding(
        self,
        text: str,
        task_type: str = "RETRIEVAL_DOCUMENT",
    ) -> List[float]:
        """
        Get a single text embedding using Vertex AI textembedding-gecko@003 model.

        Args:
            text: The text to embed.
            task_type: Task type for the embedding (RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, etc.).

        Returns:
            List of float values representing the embedding vector.
        """
        response = self.embedding_model.get_embeddings(
            texts=[text],
            task_type=task_type,
        )
        return response[0].values

    def get_embeddings(
        self,
        texts: List[str],
        task_type: str = "RETRIEVAL_DOCUMENT",
    ) -> List[List[float]]:
        """
        Get embeddings for multiple texts using Vertex AI textembedding-gecko@003.
        """
        all_embeddings = []

        batch_size = 250
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.embedding_model.get_embeddings(
                texts=batch,
                task_type=task_type,
            )
            for embedding in response:
                all_embeddings.append(embedding.values)

        return all_embeddings


def embed_ocr_sections(
    sections: List[Dict[str, Any]],
    model_name: str = GOOGLE_CLOUD_EMBEDDING_MODEL,
    task_type: str = "RETRIEVAL_DOCUMENT",
    client: Optional[VertexAIEmbeddingClient] = None,
) -> List[Dict[str, Any]]:
    """
    Embed extracted OCR document sections for semantic retrieval.

    Uses Google Cloud Vertex AI with the textembedding-gecko@003 model
    via aiplatform.googleapis.com to generate embeddings for each section.

    Args:
        sections: List of section dictionaries with 'text' and optional metadata.
        model_name: Vertex AI embedding model name.
        task_type: Embedding task type (RETRIEVAL_DOCUMENT, RETRIEVAL_QUERY, SEMANTIC_SIMILARITY, etc.).
        client: Optional pre-configured VertexAIEmbeddingClient.

    Returns:
        List of section dictionaries with added 'embedding' vectors.
    """
    if client is None:
        client = VertexAIEmbeddingClient()

    texts = [section.get("text", "") for section in sections if section.get("text", "").strip()]

    if not texts:
        return sections

    embeddings = client.get_embeddings(texts, task_type=task_type)

    result_sections = []
    embedding_idx = 0

    for section in sections:
        section_text = section.get("text", "")
        if section_text.strip():
            section_with_embedding = dict(section)
            section_with_embedding["embedding"] = embeddings[embedding_idx]
            section_with_embedding["model"] = model_name
            section_with_embedding["task_type"] = task_type
            result_sections.append(section_with_embedding)
            embedding_idx += 1
        else:
            section_with_embedding = dict(section)
            section_with_embedding["embedding"] = None
            result_sections.append(section_with_embedding)

    return result_sections


def embed_ocr_text(
    ocr_text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    model_name: str = GOOGLE_CLOUD_EMBEDDING_MODEL,
    task_type: str = "RETRIEVAL_DOCUMENT",
) -> List[Dict[str, Any]]:
    """
    Chunk and embed full OCR text for semantic retrieval.

    Uses Google Cloud Vertex AI textembedding-gecko@003 model for generating
    embeddings of document text chunks.

    Args:
        ocr_text: Full OCR-extracted text.
        chunk_size: Maximum characters per chunk.
        chunk_overlap: Number of overlapping characters between chunks.
        model_name: Vertex AI embedding model name.
        task_type: Embedding task type.

    Returns:
        List of chunk dictionaries with text and embedding vectors.
    """
    chunks = _chunk_text(ocr_text, chunk_size, chunk_overlap)

    sections = [
        {"text": chunk, "chunk_index": i, "total_chunks": len(chunks)}
        for i, chunk in enumerate(chunks)
    ]

    return embed_ocr_sections(sections, model_name, task_type)


def embed_ocr_blocks(
    blocks: list,
    task_type: str = "RETRIEVAL_DOCUMENT",
    client: Optional[VertexAIEmbeddingClient] = None,
) -> List[Dict[str, Any]]:
    """
    Embed individual OCR blocks for section-level retrieval.

    Args:
        blocks: List of OCR block objects with .text attribute or dictionaries.
        task_type: Embedding task type.
        client: Optional pre-configured client.

    Returns:
        List of block dictionaries with embeddings.
    """
    if client is None:
        client = VertexAIEmbeddingClient()

    sections = []
    for i, block in enumerate(blocks):
        if hasattr(block, 'text'):
            text = block.text
            block_type = getattr(block, 'block_type', 'TEXT')
            if hasattr(block_type, 'value'):
                block_type = block_type.value
        elif isinstance(block, dict):
            text = block.get('text', '')
            block_type = block.get('block_type', 'TEXT')
        else:
            text = str(block)
            block_type = 'TEXT'

        if text.strip():
            sections.append({
                "text": text,
                "block_index": i,
                "block_type": block_type,
            })

    return embed_ocr_sections(sections, task_type=task_type, client=client)


def _chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks for embedding."""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        if end >= len(text):
            chunks.append(text[start:])
            break

        chunk = text[start:end]

        if chunk_overlap > 0 and end < len(text):
            overlap_text = text[end - chunk_overlap:end]
            boundary = chunk.rfind('\n', 0, chunk_overlap)
            if boundary == -1:
                boundary = chunk.rfind('. ', 0, chunk_overlap)
                if boundary != -1:
                    boundary += 2
            if boundary > 0:
                chunk = text[start:start + boundary]
                end = start + boundary
            else:
                chunk = chunk.strip()

        if chunk.strip():
            chunks.append(chunk.strip())

        start = end - chunk_overlap
        if start <= 0:
            start = end

    return chunks


def compute_similarity(
    embedding1: List[float],
    embedding2: List[float],
    metric: str = "cosine",
) -> float:
    """
    Compute similarity between two embedding vectors.

    Args:
        embedding1: First embedding vector.
        embedding2: Second embedding vector.
        metric: Similarity metric (cosine, dot).

    Returns:
        Similarity score between 0 and 1.
    """
    import math

    if metric == "cosine":
        dot_product = sum(a * b for a, b in zip(embedding1, embedding2))
        norm1 = math.sqrt(sum(a * a for a in embedding1))
        norm2 = math.sqrt(sum(b * b for b in embedding2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot_product / (norm1 * norm2)
    elif metric == "dot":
        return sum(a * b for a, b in zip(embedding1, embedding2))
    else:
        raise ValueError(f"Unknown metric: {metric}")


def search_embeddings(
    query_text: str,
    embedded_sections: List[Dict[str, Any]],
    top_k: int = 5,
    threshold: float = 0.5,
    task_type: str = "RETRIEVAL_QUERY",
) -> List[Dict[str, Any]]:
    """
    Search embedded document sections using a query.

    Uses Google Cloud Vertex AI textembedding-gecko@003 to embed the query
    and compute cosine similarity against section embeddings.

    Args:
        query_text: The search query text.
        embedded_sections: List of pre-embedded section dictionaries.
        top_k: Number of top results to return.
        threshold: Minimum similarity score threshold.
        task_type: Embedding task type for query.

    Returns:
        List of matching sections sorted by similarity score.
    """
    client = VertexAIEmbeddingClient()

    query_embedding = client.get_embedding(query_text, task_type=task_type)

    results = []
    for section in embedded_sections:
        section_embedding = section.get("embedding")
        if section_embedding is None:
            continue

        similarity = compute_similarity(query_embedding, section_embedding)
        if similarity >= threshold:
            result = dict(section)
            result["similarity_score"] = similarity
            results.append(result)

    results.sort(key=lambda x: x["similarity_score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    sample_sections = [
        {"text": "Invoice #12345 dated January 15, 2024", "section": "header"},
        {"text": "Total amount due: $1,500.00 for consulting services", "section": "body"},
        {"text": "Payment terms: Net 30 days from invoice date", "section": "footer"},
    ]

    embedded = embed_ocr_sections(sample_sections)
    for section in embedded:
        emb = section.get("embedding")
        print(f"Section '{section['section']}': embedding length = {len(emb) if emb else 0}")
