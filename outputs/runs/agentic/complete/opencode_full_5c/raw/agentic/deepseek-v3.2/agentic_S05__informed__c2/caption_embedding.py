import openai
import os
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime
import json


class CaptionEmbedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = model
        self.embeddings_cache = {}

        self.available_models = [
            "text-embedding-3-small",
            "text-embedding-3-large",
            "text-embedding-ada-002",
        ]

    def validate_model(self) -> bool:
        return self.model in self.available_models

    def embed_text(self, text: str) -> Optional[np.ndarray]:
        if not text or not text.strip():
            return None

        cache_key = f"{self.model}:{text[:100]}"
        if cache_key in self.embeddings_cache:
            return self.embeddings_cache[cache_key]

        try:
            response = self.client.embeddings.create(
                model=self.model, input=text, encoding_format="float"
            )

            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            self.embeddings_cache[cache_key] = embedding

            return embedding

        except Exception as e:
            print(f"Embedding error: {e}")
            return None

    def embed_caption(self, caption: Dict[str, Any]) -> Dict[str, Any]:
        text = caption.get("text", "")
        is_final = caption.get("is_final", False)

        embedding = self.embed_text(text)

        result = {
            "caption": caption,
            "embedding": embedding.tolist() if embedding is not None else None,
            "embedding_model": self.model,
            "embedding_dimensions": len(embedding) if embedding is not None else 0,
            "is_final": is_final,
            "timestamp": caption.get("timestamp", datetime.now().isoformat()),
            "has_embedding": embedding is not None,
        }

        return result

    def embed_caption_batch(
        self, captions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        texts = [caption.get("text", "") for caption in captions]
        valid_indices = [i for i, text in enumerate(texts) if text and text.strip()]
        valid_texts = [texts[i] for i in valid_indices]

        if not valid_texts:
            return []

        try:
            response = self.client.embeddings.create(
                model=self.model, input=valid_texts, encoding_format="float"
            )

            results = []
            for idx, caption_idx in enumerate(valid_indices):
                caption = captions[caption_idx]
                embedding = np.array(response.data[idx].embedding, dtype=np.float32)

                result = {
                    "caption": caption,
                    "embedding": embedding.tolist(),
                    "embedding_model": self.model,
                    "embedding_dimensions": len(embedding),
                    "is_final": caption.get("is_final", False),
                    "timestamp": caption.get("timestamp", datetime.now().isoformat()),
                    "has_embedding": True,
                }
                results.append(result)

            return results

        except Exception as e:
            print(f"Batch embedding error: {e}")
            return []

    def calculate_similarity(
        self, embedding1: np.ndarray, embedding2: np.ndarray
    ) -> float:
        if embedding1 is None or embedding2 is None:
            return 0.0

        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        similarity = np.dot(embedding1, embedding2) / (norm1 * norm2)
        return float(similarity)

    def find_similar_captions(
        self,
        query_caption: Dict[str, Any],
        caption_pool: List[Dict[str, Any]],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embed_text(query_caption.get("text", ""))
        if query_embedding is None:
            return []

        similarities = []

        for caption in caption_pool:
            caption_embedding = None
            if "embedding" in caption:
                caption_embedding = np.array(caption["embedding"], dtype=np.float32)
            else:
                caption_embedding = self.embed_text(caption.get("text", ""))

            if caption_embedding is not None:
                similarity = self.calculate_similarity(
                    query_embedding, caption_embedding
                )
                similarities.append((similarity, caption))

        similarities.sort(key=lambda x: x[0], reverse=True)

        return [
            {"caption": caption, "similarity_score": similarity, "rank": i + 1}
            for i, (similarity, caption) in enumerate(similarities[:top_k])
        ]

    def cluster_captions(
        self, captions: List[Dict[str, Any]], n_clusters: int = 3
    ) -> Dict[str, Any]:
        from sklearn.cluster import KMeans

        embeddings = []
        valid_captions = []

        for caption in captions:
            embedding = self.embed_text(caption.get("text", ""))
            if embedding is not None:
                embeddings.append(embedding)
                valid_captions.append(caption)

        if len(embeddings) < n_clusters:
            return {"error": f"Not enough embeddings for {n_clusters} clusters"}

        embeddings_array = np.array(embeddings)

        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings_array)

        clusters = {}
        for i, (caption, label) in enumerate(zip(valid_captions, cluster_labels)):
            if label not in clusters:
                clusters[label] = {
                    "captions": [],
                    "centroid": kmeans.cluster_centers_[label].tolist(),
                    "size": 0,
                }
            clusters[label]["captions"].append(caption)
            clusters[label]["size"] += 1

        for label in clusters:
            cluster_texts = [c.get("text", "") for c in clusters[label]["captions"]]
            clusters[label]["representative_text"] = self._find_representative_text(
                cluster_texts, embeddings_array[cluster_labels == label]
            )

        return {
            "clusters": clusters,
            "total_captions": len(valid_captions),
            "n_clusters": n_clusters,
            "inertia": float(kmeans.inertia_),
        }

    def _find_representative_text(
        self, texts: List[str], embeddings: np.ndarray
    ) -> str:
        if not texts:
            return ""

        centroid = np.mean(embeddings, axis=0)
        similarities = [self.calculate_similarity(centroid, emb) for emb in embeddings]

        most_similar_idx = np.argmax(similarities)
        return texts[most_similar_idx]

    def create_semantic_index(self, captions: List[Dict[str, Any]]) -> Dict[str, Any]:
        embedded_captions = self.embed_caption_batch(captions)

        index = {
            "captions": embedded_captions,
            "total_embeddings": len(embedded_captions),
            "model": self.model,
            "created_at": datetime.now().isoformat(),
            "embedding_dimensions": embedded_captions[0]["embedding_dimensions"]
            if embedded_captions
            else 0,
        }

        return index

    def semantic_search(
        self, query: str, index: Dict[str, Any], top_k: int = 5
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embed_text(query)
        if query_embedding is None:
            return []

        similarities = []

        for caption_data in index.get("captions", []):
            if caption_data.get("has_embedding"):
                caption_embedding = np.array(
                    caption_data["embedding"], dtype=np.float32
                )
                similarity = self.calculate_similarity(
                    query_embedding, caption_embedding
                )
                similarities.append((similarity, caption_data))

        similarities.sort(key=lambda x: x[0], reverse=True)

        return [
            {"caption": item[1]["caption"], "similarity_score": item[0], "rank": i + 1}
            for i, item in enumerate(similarities[:top_k])
        ]

    def set_model(self, model: str):
        if model not in self.available_models:
            raise ValueError(
                f"Unsupported model: {model}. Available: {self.available_models}"
            )
        self.model = model

    def get_available_models(self) -> List[str]:
        return self.available_models.copy()

    def clear_cache(self):
        self.embeddings_cache.clear()
