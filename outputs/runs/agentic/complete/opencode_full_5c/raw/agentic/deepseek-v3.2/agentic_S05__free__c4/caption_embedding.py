from openai import OpenAI
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class CaptionEmbedder:
    def __init__(
        self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"
    ):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed_text(self, text: str) -> Dict[str, Any]:
        response = self.client.embeddings.create(model=self.model, input=text)

        embedding = response.data[0].embedding

        return {
            "embedding": embedding,
            "model": self.model,
            "text": text,
            "embedding_dim": len(embedding),
            "timestamp": datetime.now().isoformat(),
        }

    def embed_caption(self, caption: str, is_final: bool = True) -> Dict[str, Any]:
        embedding_result = self.embed_text(caption)

        return {**embedding_result, "is_final": is_final, "caption": caption}

    async def embed_stream(self, caption_stream):
        async for caption, is_final in caption_stream:
            embedding = self.embed_caption(caption, is_final)
            yield embedding

    def batch_embed(self, captions: List[str]) -> List[Dict[str, Any]]:
        if not captions:
            return []

        response = self.client.embeddings.create(model=self.model, input=captions)

        embeddings = []
        for i, data in enumerate(response.data):
            embeddings.append(
                {
                    "embedding": data.embedding,
                    "model": self.model,
                    "text": captions[i],
                    "embedding_dim": len(data.embedding),
                    "index": i,
                    "timestamp": datetime.now().isoformat(),
                }
            )

        return embeddings

    def similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = np.dot(vec1, vec2) / (norm1 * norm2)
        return float(similarity)

    def find_similar_captions(
        self, query: str, captions: List[Dict[str, Any]], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embed_text(query)["embedding"]

        similarities = []
        for caption_data in captions:
            if "embedding" in caption_data:
                sim = self.similarity(query_embedding, caption_data["embedding"])
                similarities.append(
                    {
                        "caption": caption_data.get(
                            "text", caption_data.get("caption", "")
                        ),
                        "similarity": sim,
                        "metadata": caption_data,
                    }
                )

        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]

    def cluster_captions(
        self, captions: List[Dict[str, Any]], n_clusters: int = 3
    ) -> Dict[str, Any]:
        from sklearn.cluster import KMeans
        import numpy as np

        embeddings = []
        valid_captions = []

        for caption_data in captions:
            if "embedding" in caption_data:
                embeddings.append(caption_data["embedding"])
                valid_captions.append(caption_data)

        if not embeddings:
            return {"clusters": [], "error": "No valid embeddings found"}

        embeddings_array = np.array(embeddings)

        kmeans = KMeans(n_clusters=min(n_clusters, len(embeddings)), random_state=42)
        clusters = kmeans.fit_predict(embeddings_array)

        results = []
        for i, caption_data in enumerate(valid_captions):
            results.append(
                {
                    "caption": caption_data.get(
                        "text", caption_data.get("caption", "")
                    ),
                    "cluster": int(clusters[i]),
                    "embedding": embeddings[i],
                    "distance_to_center": float(
                        np.linalg.norm(
                            embeddings_array[i] - kmeans.cluster_centers_[clusters[i]]
                        )
                    ),
                }
            )

        cluster_summaries = {}
        for cluster_id in range(n_clusters):
            cluster_captions = [
                r["caption"] for r in results if r["cluster"] == cluster_id
            ]
            if cluster_captions:
                cluster_summaries[cluster_id] = {
                    "size": len(cluster_captions),
                    "sample_captions": cluster_captions[:3],
                    "center": kmeans.cluster_centers_[cluster_id].tolist()
                    if cluster_id < len(kmeans.cluster_centers_)
                    else [],
                }

        return {
            "clusters": results,
            "cluster_summaries": cluster_summaries,
            "n_clusters": n_clusters,
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
        }

    def semantic_search(
        self, meeting_transcript: str, query: str, chunk_size: int = 100
    ) -> Dict[str, Any]:
        words = meeting_transcript.split()
        chunks = []

        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i : i + chunk_size])
            chunks.append(chunk)

        chunk_embeddings = self.batch_embed(chunks)
        query_embedding = self.embed_text(query)["embedding"]

        results = []
        for i, chunk_data in enumerate(chunk_embeddings):
            sim = self.similarity(query_embedding, chunk_data["embedding"])
            results.append(
                {
                    "chunk": chunks[i],
                    "similarity": sim,
                    "start_word": i * chunk_size,
                    "end_word": min((i + 1) * chunk_size, len(words)),
                }
            )

        results.sort(key=lambda x: x["similarity"], reverse=True)

        return {
            "query": query,
            "top_matches": results[:5],
            "total_chunks": len(chunks),
            "model": self.model,
            "timestamp": datetime.now().isoformat(),
        }

    def save_embeddings(self, embeddings: List[Dict[str, Any]], filename: str):
        serializable = []
        for emb in embeddings:
            serializable.append(
                {
                    "embedding": emb["embedding"],
                    "text": emb.get("text", emb.get("caption", "")),
                    "model": emb.get("model", self.model),
                    "timestamp": emb.get("timestamp", datetime.now().isoformat()),
                    "metadata": {
                        k: v
                        for k, v in emb.items()
                        if k not in ["embedding", "text", "model", "timestamp"]
                    },
                }
            )

        with open(filename, "w") as f:
            json.dump(serializable, f, indent=2)

    def load_embeddings(self, filename: str) -> List[Dict[str, Any]]:
        with open(filename, "r") as f:
            data = json.load(f)

        embeddings = []
        for item in data:
            embeddings.append(
                {
                    "embedding": item["embedding"],
                    "text": item["text"],
                    "model": item.get("model", self.model),
                    "timestamp": item.get("timestamp"),
                    **item.get("metadata", {}),
                }
            )

        return embeddings
