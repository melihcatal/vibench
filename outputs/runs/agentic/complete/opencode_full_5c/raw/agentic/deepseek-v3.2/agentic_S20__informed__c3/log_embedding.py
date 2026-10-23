import os
import json
import numpy as np
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dataclasses import dataclass


@dataclass
class LogEmbedding:
    """Log message embedding container."""

    log_message: str
    embedding: List[float]
    model: str
    dimensions: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "log_message": self.log_message,
            "embedding_preview": self.embedding[:5] if self.embedding else [],
            "embedding_dimensions": self.dimensions,
            "model": self.model,
        }


class LogEmbeddingGenerator:
    """Embed selected log messages for semantic retrieval using OpenAI embeddings."""

    def __init__(
        self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"
    ):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def embed_log_message(self, message: str) -> LogEmbedding:
        """Generate embedding for a single log message."""
        try:
            response = self.client.embeddings.create(
                model=self.model, input=message, encoding_format="float"
            )

            embedding = response.data[0].embedding

            return LogEmbedding(
                log_message=message,
                embedding=embedding,
                model=self.model,
                dimensions=len(embedding),
            )

        except Exception as e:
            print(f"Embedding error: {e}")
            raise

    def embed_log_messages(self, messages: List[str]) -> List[LogEmbedding]:
        """Generate embeddings for multiple log messages."""
        embeddings = []

        for message in messages:
            try:
                embedding = self.embed_log_message(message)
                embeddings.append(embedding)
            except Exception as e:
                print(f"Failed to embed message '{message[:50]}...': {e}")

        print(
            f"Generated embeddings for {len(embeddings)}/{len(messages)} log messages"
        )
        return embeddings

    def embed_error_logs(
        self, error_logs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Embed error logs with their metadata."""
        messages = []
        log_contexts = []

        for log in error_logs:
            payload = log.get("payload", {})
            if isinstance(payload, dict):
                message = payload.get("message", str(payload))
            else:
                message = str(payload)

            messages.append(message)
            log_contexts.append({"original_log": log, "message": message})

        embeddings = self.embed_log_messages(messages)

        results = []
        for i, (context, embedding) in enumerate(zip(log_contexts, embeddings)):
            result = context["original_log"].copy()
            result["embedding"] = {
                "vector": embedding.embedding,
                "model": embedding.model,
                "dimensions": embedding.dimensions,
            }
            result["embedded_message"] = embedding.log_message
            results.append(result)

        return results

    def similarity_search(
        self, query: str, embeddings: List[LogEmbedding], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Find most similar log messages to a query."""
        try:
            query_embedding = self.embed_log_message(query)

            similarities = []
            for emb in embeddings:
                similarity = self._cosine_similarity(
                    query_embedding.embedding, emb.embedding
                )
                similarities.append(
                    {
                        "log_message": emb.log_message,
                        "similarity": similarity,
                        "embedding": emb,
                    }
                )

            similarities.sort(key=lambda x: x["similarity"], reverse=True)

            return similarities[:top_k]

        except Exception as e:
            print(f"Similarity search error: {e}")
            return []

    def find_similar_errors(
        self, error_message: str, error_logs: List[Dict[str, Any]], top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """Find similar historical errors for a new error message."""
        embeddings = self.embed_error_logs(error_logs)

        log_embeddings = []
        for emb_result in embeddings:
            if "embedding" in emb_result:
                log_embeddings.append(
                    LogEmbedding(
                        log_message=emb_result.get("embedded_message", ""),
                        embedding=emb_result["embedding"]["vector"],
                        model=emb_result["embedding"]["model"],
                        dimensions=emb_result["embedding"]["dimensions"],
                    )
                )

        similar_results = self.similarity_search(error_message, log_embeddings, top_k)

        return similar_results

    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            raise ValueError("Vectors must have the same dimensions")

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)


def create_log_embeddings_for_semantic_search(
    log_messages: List[str],
) -> Dict[str, Any]:
    """Create embeddings for log messages to enable semantic search."""
    generator = LogEmbeddingGenerator()

    embeddings = generator.embed_log_messages(log_messages)

    return {
        "total_messages": len(log_messages),
        "successfully_embedded": len(embeddings),
        "embedding_model": generator.model,
        "embeddings": [emb.to_dict() for emb in embeddings],
    }


if __name__ == "__main__":
    print("Testing log message embeddings with OpenAI API...")

    test_messages = [
        "Database connection timeout after 30 seconds",
        "Authentication failed: Invalid password for user admin",
        "Payment processing error: Credit card declined",
        "Memory usage exceeded 90% threshold on server-01",
        "File upload failed: File size exceeds 10MB limit",
        "API rate limit exceeded for IP 192.168.1.100",
        "SSL certificate expired for domain example.com",
        "Disk space critical: Only 1GB remaining on /var",
    ]

    try:
        generator = LogEmbeddingGenerator()

        print(
            f"\nGenerating embeddings for {len(test_messages)} log messages using {generator.model}..."
        )
        embeddings = generator.embed_log_messages(test_messages)

        print(f"\nGenerated {len(embeddings)} embeddings")
        if embeddings:
            print(f"Embedding dimensions: {embeddings[0].dimensions}")
            print(f"Model: {embeddings[0].model}")

        query = "database connection problem"
        print(f"\nSearching for logs similar to: '{query}'")

        similar_logs = generator.similarity_search(query, embeddings, top_k=3)

        print(f"\nTop {len(similar_logs)} similar logs:")
        for i, result in enumerate(similar_logs):
            print(f"\n{i + 1}. Similarity: {result['similarity']:.3f}")
            print(f"   Message: {result['log_message'][:80]}...")

    except Exception as e:
        print(f"Test failed: {e}")
        print("Note: OPENAI_API_KEY environment variable must be set for this test")
