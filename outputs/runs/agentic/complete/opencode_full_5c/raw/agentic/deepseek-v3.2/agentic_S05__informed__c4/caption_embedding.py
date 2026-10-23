import os
from typing import List, Dict, Any, Optional
import numpy as np
import openai


class CaptionEmbedder:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Set OPENAI_API_KEY environment variable."
            )

        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = "text-embedding-3-small"
        self.embedding_dim = 1536

    def embed_caption(self, caption_text: str) -> Dict[str, Any]:
        """Generate embedding for a single caption."""
        try:
            response = self.client.embeddings.create(
                model=self.model, input=caption_text, encoding_format="float"
            )

            embedding = response.data[0].embedding

            return {
                "text": caption_text,
                "embedding": embedding,
                "model": self.model,
                "dimensions": len(embedding),
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }

        except Exception as e:
            print(f"Error embedding caption: {e}")
            return {"text": caption_text, "embedding": None, "error": str(e)}

    def embed_captions_batch(self, captions: List[str]) -> List[Dict[str, Any]]:
        """Generate embeddings for multiple captions."""
        if not captions:
            return []

        try:
            response = self.client.embeddings.create(
                model=self.model, input=captions, encoding_format="float"
            )

            results = []
            for i, data in enumerate(response.data):
                results.append(
                    {
                        "text": captions[i],
                        "embedding": data.embedding,
                        "model": self.model,
                        "dimensions": len(data.embedding),
                        "index": i,
                    }
                )

            return results

        except Exception as e:
            print(f"Error embedding captions batch: {e}")
            return [self.embed_caption(caption) for caption in captions]

    def embed_caption_objects(
        self, caption_objects: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate embeddings for caption objects."""
        texts = [obj.get("text", "") for obj in caption_objects]
        embeddings = self.embed_captions_batch(texts)

        results = []
        for i, (caption_obj, embedding_result) in enumerate(
            zip(caption_objects, embeddings)
        ):
            result = {**caption_obj, "embedding_result": embedding_result}
            results.append(result)

        return results


class SemanticMeetingSearch:
    def __init__(self, embedder: CaptionEmbedder):
        self.embedder = embedder
        self.caption_embeddings = []
        self.caption_texts = []

    def add_caption(self, caption: Dict[str, Any]):
        """Add a caption to the search index."""
        embedding_result = self.embedder.embed_caption(caption.get("text", ""))

        if embedding_result.get("embedding"):
            self.caption_embeddings.append(embedding_result["embedding"])
            self.caption_texts.append(
                {
                    "text": caption.get("text", ""),
                    "timestamp": caption.get("timestamp"),
                    "speaker": caption.get("speaker"),
                    "original_caption": caption,
                }
            )

    def add_captions_batch(self, captions: List[Dict[str, Any]]):
        """Add multiple captions to the search index."""
        for caption in captions:
            self.add_caption(caption)

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for similar captions using semantic similarity."""
        query_embedding_result = self.embedder.embed_caption(query)

        if not query_embedding_result.get("embedding"):
            return []

        query_embedding = np.array(query_embedding_result["embedding"])

        if not self.caption_embeddings:
            return []

        # Calculate cosine similarities
        similarities = []
        for i, caption_embedding in enumerate(self.caption_embeddings):
            caption_vec = np.array(caption_embedding)
            similarity = np.dot(query_embedding, caption_vec) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(caption_vec)
            )
            similarities.append((i, similarity))

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top-k results
        results = []
        for idx, similarity in similarities[:top_k]:
            caption_info = self.caption_texts[idx]
            results.append(
                {
                    **caption_info,
                    "similarity": float(similarity),
                    "rank": len(results) + 1,
                }
            )

        return results

    def find_similar_captions(
        self, caption_text: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """Find captions similar to the given caption text."""
        return self.search(caption_text, top_k)

    def cluster_captions(self, n_clusters: int = 5) -> Dict[str, Any]:
        """Cluster captions into topics."""
        if not self.caption_embeddings or len(self.caption_embeddings) < n_clusters:
            return {"clusters": [], "error": "Not enough captions for clustering"}

        try:
            from sklearn.cluster import KMeans

            embeddings_array = np.array(self.caption_embeddings)

            kmeans = KMeans(
                n_clusters=min(n_clusters, len(self.caption_embeddings)),
                random_state=42,
            )
            cluster_labels = kmeans.fit_predict(embeddings_array)

            # Organize captions by cluster
            clusters = {}
            for i, label in enumerate(cluster_labels):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(self.caption_texts[i])

            # Get cluster centroids
            centroids = kmeans.cluster_centers_

            # Find representative captions for each cluster
            representative_captions = {}
            for label in clusters:
                cluster_embeddings = embeddings_array[cluster_labels == label]
                centroid = centroids[label]

                # Find caption closest to centroid
                distances = np.linalg.norm(cluster_embeddings - centroid, axis=1)
                closest_idx = np.argmin(distances)

                # Map back to original index
                cluster_indices = np.where(cluster_labels == label)[0]
                representative_idx = cluster_indices[closest_idx]

                representative_captions[label] = self.caption_texts[representative_idx]

            return {
                "clusters": clusters,
                "centroids": centroids.tolist(),
                "representative_captions": representative_captions,
                "cluster_sizes": {
                    label: len(captions) for label, captions in clusters.items()
                },
            }

        except ImportError:
            return {"clusters": [], "error": "scikit-learn not installed"}
        except Exception as e:
            return {"clusters": [], "error": str(e)}


async def embed_live_caption_stream(caption_stream, embedder: CaptionEmbedder):
    """Embed captions from a live stream."""
    async for caption in caption_stream:
        if caption.get("is_final", False):
            caption_text = caption.get("text", "")

            if caption_text.strip():
                embedding_result = embedder.embed_caption(caption_text)

                yield {"caption": caption, "embedding": embedding_result}


if __name__ == "__main__":
    embedder = CaptionEmbedder()

    test_captions = [
        "Let's discuss the project timeline for Q4.",
        "We need to address the security vulnerabilities in the API.",
        "The marketing team will launch the campaign next Monday.",
        "Technical debt is accumulating and needs refactoring.",
    ]

    print("Testing caption embeddings...")
    for caption in test_captions:
        result = embedder.embed_caption(caption)
        print(f"Caption: {caption[:50]}...")
        print(f"Embedding dimensions: {result.get('dimensions', 0)}")
        print(f"Model: {result.get('model', 'N/A')}")
        print()

    # Test semantic search
    search_engine = SemanticMeetingSearch(embedder)
    search_engine.add_captions_batch([{"text": caption} for caption in test_captions])

    query = "When is the marketing campaign starting?"
    results = search_engine.search(query)

    print(f"Search results for: '{query}'")
    for result in results:
        print(f"- {result['text']} (similarity: {result['similarity']:.3f})")
