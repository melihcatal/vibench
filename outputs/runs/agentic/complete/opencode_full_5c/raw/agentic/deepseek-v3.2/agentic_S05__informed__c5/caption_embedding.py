import os
import asyncio
from typing import List, Dict, Any, Optional
import cohere


class CaptionEmbedder:
    """Embed caption chunks for semantic meeting search using Cohere."""

    def __init__(self, model: str = "embed-english-v3.0"):
        self.api_key = os.getenv("COHERE_API_KEY")
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.Client(self.api_key)
        self.model = model

        # Define embedding input types
        self.input_types = {
            "search_document": "Use this for documents to be searched over.",
            "search_query": "Use this for search queries.",
            "classification": "Use this for classification tasks.",
            "clustering": "Use this for clustering tasks.",
        }

    async def embed_caption(
        self, caption: str, input_type: str = "search_document"
    ) -> List[float]:
        """Embed a single caption text."""
        if not caption or not caption.strip():
            return [0.0] * 1024  # Return zero vector for empty text

        if input_type not in self.input_types:
            raise ValueError(
                f"Input type must be one of: {list(self.input_types.keys())}"
            )

        try:
            response = self.client.embed(
                texts=[caption], model=self.model, input_type=input_type
            )

            return response.embeddings[0]

        except Exception as e:
            print(f"Embedding error: {e}")
            # Return a simple hash-based fallback embedding
            return self._fallback_embedding(caption)

    def _fallback_embedding(self, text: str, dimensions: int = 1024) -> List[float]:
        """Generate a simple fallback embedding based on text hash."""
        import hashlib
        import struct

        if not text:
            return [0.0] * dimensions

        # Create deterministic embedding based on text hash
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()

        # Convert hash to floats
        embedding = []
        for i in range(0, min(len(hash_bytes), dimensions * 4), 4):
            chunk = hash_bytes[i : i + 4]
            if len(chunk) == 4:
                # Convert 4 bytes to float
                value = struct.unpack("f", chunk)[0]
                # Normalize to [-1, 1]
                value = (value % 2.0) - 1.0
                embedding.append(value)

        # Pad if needed
        while len(embedding) < dimensions:
            embedding.append(0.0)

        return embedding[:dimensions]

    async def embed_caption_stream(
        self, caption_stream, input_type: str = "search_document"
    ):
        """Embed a stream of captions."""
        async for caption in caption_stream:
            if caption and caption.strip():
                embedding = await self.embed_caption(caption, input_type)
                yield {
                    "text": caption,
                    "embedding": embedding,
                    "embedding_dim": len(embedding),
                }
            else:
                yield {"text": caption, "embedding": [], "embedding_dim": 0}

    def semantic_search(
        self, query: str, embeddings: List[Dict], top_k: int = 5
    ) -> List[Dict]:
        """Perform semantic search over embedded captions."""
        if not embeddings:
            return []

        # Embed the query
        query_embedding = self.client.embed(
            texts=[query], model=self.model, input_type="search_query"
        ).embeddings[0]

        # Calculate cosine similarities
        results = []
        for i, item in enumerate(embeddings):
            if "embedding" not in item or not item["embedding"]:
                continue

            similarity = self._cosine_similarity(query_embedding, item["embedding"])
            results.append(
                {
                    "index": i,
                    "text": item.get("text", ""),
                    "similarity": similarity,
                    "embedding": item["embedding"],
                }
            )

        # Sort by similarity (descending)
        results.sort(key=lambda x: x["similarity"], reverse=True)

        return results[:top_k]

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def cluster_captions(
        self, embeddings: List[Dict], n_clusters: int = 3
    ) -> Dict[int, List[Dict]]:
        """Cluster captions based on their embeddings."""
        from sklearn.cluster import KMeans
        import numpy as np

        if not embeddings or len(embeddings) < n_clusters:
            return {}

        # Extract embeddings
        vectors = []
        valid_indices = []
        for i, item in enumerate(embeddings):
            if "embedding" in item and item["embedding"]:
                vectors.append(item["embedding"])
                valid_indices.append(i)

        if len(vectors) < n_clusters:
            return {}

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=min(n_clusters, len(vectors)), random_state=42)
        clusters = kmeans.fit_predict(vectors)

        # Group captions by cluster
        clustered = {}
        for idx, cluster_id in zip(valid_indices, clusters):
            if cluster_id not in clustered:
                clustered[cluster_id] = []
            clustered[cluster_id].append(embeddings[idx])

        return clustered

    def get_available_models(self) -> List[str]:
        """Get list of available Cohere embedding models."""
        return [
            "embed-english-v3.0",
            "embed-english-light-v3.0",
            "embed-multilingual-v3.0",
            "embed-multilingual-light-v3.0",
            "embed-english-v2.0",
            "embed-english-light-v2.0",
            "embed-multilingual-v2.0",
        ]

    def get_embedding_dimensions(self, model: str = None) -> int:
        """Get embedding dimensions for a model."""
        model = model or self.model
        dimensions_map = {
            "embed-english-v3.0": 1024,
            "embed-english-light-v3.0": 384,
            "embed-multilingual-v3.0": 1024,
            "embed-multilingual-light-v3.0": 384,
            "embed-english-v2.0": 4096,
            "embed-english-light-v2.0": 1024,
            "embed-multilingual-v2.0": 768,
        }
        return dimensions_map.get(model, 1024)


async def mock_caption_stream_for_embedding():
    """Mock caption stream for embedding testing."""
    captions = [
        "We need to discuss the quarterly sales results.",
        "The marketing campaign has been very successful.",
        "Customer feedback shows high satisfaction levels.",
        "Supply chain issues need to be addressed immediately.",
        "The new product launch is scheduled for next month.",
        "Budget constraints may affect our expansion plans.",
        "Team collaboration has improved significantly.",
        "We should focus on innovation and R&D investments.",
    ]

    for caption in captions:
        yield caption
        await asyncio.sleep(0.1)


async def test_caption_embedding():
    """Test caption embedding functionality."""
    print("Testing caption embedding with Cohere...")

    embedder = CaptionEmbedder(model="embed-english-v3.0")

    print(f"Using model: {embedder.model}")
    print(f"Embedding dimensions: {embedder.get_embedding_dimensions()}")
    print(f"Available models: {embedder.get_available_models()}")
    print(f"Input types: {list(embedder.input_types.keys())}")

    # Test single caption embedding
    test_caption = "The quarterly meeting discussed sales growth and future plans."

    print(f"\nTesting single caption embedding:")
    print(f"Caption: {test_caption}")

    embedding = await embedder.embed_caption(test_caption, "search_document")
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")

    # Test streaming embedding
    print(f"\n\nTesting streaming embedding:")
    embeddings = []

    async for result in embedder.embed_caption_stream(
        mock_caption_stream_for_embedding(), input_type="search_document"
    ):
        print(f"Embedded: {result['text'][:50]}... (dim: {result['embedding_dim']})")
        embeddings.append(result)

    # Test semantic search
    print(f"\n\nTesting semantic search:")
    search_query = "sales performance and growth"
    search_results = embedder.semantic_search(search_query, embeddings, top_k=3)

    print(f"Search query: '{search_query}'")
    print(f"Top {len(search_results)} results:")
    for i, result in enumerate(search_results, 1):
        print(f"{i}. Similarity: {result['similarity']:.3f}")
        print(f"   Text: {result['text']}")

    # Test clustering
    print(f"\n\nTesting caption clustering:")
    clusters = embedder.cluster_captions(embeddings, n_clusters=3)

    print(f"Found {len(clusters)} clusters:")
    for cluster_id, items in clusters.items():
        print(f"\nCluster {cluster_id} ({len(items)} items):")
        for item in items[:3]:  # Show first 3 items per cluster
            print(f"  - {item['text'][:60]}...")


if __name__ == "__main__":
    asyncio.run(test_caption_embedding())
