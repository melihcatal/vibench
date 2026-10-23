import os
from typing import List, Dict, Any, Optional
import openai
from document_models import TextExtractionResponse, LayoutBlock


class OCREmbeddingGenerator:
    """Embed extracted document sections for semantic retrieval using OpenAI Embeddings."""

    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = openai.OpenAI(api_key=api_key)
        self.model = "text-embedding-3-small"

    def generate_embedding(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Generate embedding for a single text using OpenAI Embeddings API.
        """
        response = self.client.embeddings.create(
            model=model or self.model, input=text, encoding_format="float"
        )

        return response.data[0].embedding

    def generate_document_embeddings(
        self,
        extraction_response: TextExtractionResponse,
        chunk_size: int = 1000,
        overlap: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for document text by chunking.
        """
        text = extraction_response.text
        chunks = self._chunk_text(text, chunk_size, overlap)

        embeddings = []
        for i, chunk in enumerate(chunks):
            embedding = self.generate_embedding(chunk)
            embeddings.append(
                {
                    "chunk_index": i,
                    "text": chunk,
                    "embedding": embedding,
                    "start_char": i * (chunk_size - overlap),
                    "end_char": min(i * (chunk_size - overlap) + chunk_size, len(text)),
                }
            )

        return {
            "embeddings": embeddings,
            "chunk_count": len(chunks),
            "provider": "openai_embeddings",
            "model": self.model,
            "original_extraction": extraction_response,
        }

    def generate_layout_embeddings(
        self, blocks: List[LayoutBlock], include_block_type: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate embeddings for layout blocks.
        """
        embeddings = []

        for i, block in enumerate(blocks):
            text_to_embed = block.text
            if include_block_type:
                text_to_embed = f"[{block.block_type}] {block.text}"

            embedding = self.generate_embedding(text_to_embed)

            embeddings.append(
                {
                    "block_index": i,
                    "text": block.text,
                    "embedding": embedding,
                    "block_type": block.block_type,
                    "confidence": block.confidence,
                    "page_number": block.page_number,
                }
            )

        return {
            "embeddings": embeddings,
            "block_count": len(blocks),
            "provider": "openai_embeddings",
            "model": self.model,
        }

    def batch_generate_embeddings(
        self, texts: List[str], model: Optional[str] = None
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.
        """
        response = self.client.embeddings.create(
            model=model or self.model, input=texts, encoding_format="float"
        )

        return [data.embedding for data in response.data]

    def semantic_search(
        self, query: str, embeddings: List[Dict[str, Any]], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search over embedded document chunks.
        """
        query_embedding = self.generate_embedding(query)

        scored_results = []
        for item in embeddings:
            if "embedding" not in item:
                continue

            similarity = self._cosine_similarity(query_embedding, item["embedding"])
            scored_results.append({**item, "similarity": similarity})

        scored_results.sort(key=lambda x: x["similarity"], reverse=True)
        return scored_results[:top_k]

    def _chunk_text(self, text: str, chunk_size: int, overlap: int) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import math

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)
