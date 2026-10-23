from typing import Optional, Dict, Any, List, Generator
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import asyncio
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class CaptionEmbedding:
    caption: Dict[str, Any]
    embedding: np.ndarray
    timestamp: datetime
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "caption": self.caption,
            "embedding": self.embedding.tolist(),
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CaptionEmbedding":
        return cls(
            caption=data["caption"],
            embedding=np.array(data["embedding"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            metadata=data["metadata"],
        )


class CaptionEmbedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", device: str = "cpu"):

        self.model = SentenceTransformer(model_name, device=device)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        self.embeddings_index = faiss.IndexFlatL2(self.embedding_dim)
        self.caption_store = []

    def embed_caption(
        self, caption: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None
    ) -> CaptionEmbedding:

        transcript = caption.get("transcript", "")

        if not transcript.strip():
            embedding = np.zeros(self.embedding_dim, dtype=np.float32)
        else:
            embedding = self.model.encode(transcript, convert_to_numpy=True)

        if metadata is None:
            metadata = {}

        metadata.update(
            {
                "language_code": caption.get("language_code", "en"),
                "is_final": caption.get("is_final", False),
                "speaker_tag": caption.get("speaker_tag"),
                "confidence": caption.get("confidence"),
            }
        )

        caption_embedding = CaptionEmbedding(
            caption=caption,
            embedding=embedding,
            timestamp=datetime.now(),
            metadata=metadata,
        )

        self._add_to_index(caption_embedding)

        return caption_embedding

    def _add_to_index(self, caption_embedding: CaptionEmbedding):
        embedding_array = caption_embedding.embedding.reshape(1, -1).astype("float32")
        self.embeddings_index.add(embedding_array)
        self.caption_store.append(caption_embedding)

    def embed_caption_stream(
        self,
        caption_stream: Generator[Dict[str, Any], None, None],
        embed_final_only: bool = True,
    ) -> Generator[CaptionEmbedding, None, None]:

        for caption in caption_stream:
            if embed_final_only and not caption.get("is_final", False):
                continue

            transcript = caption.get("transcript", "")
            if not transcript.strip():
                continue

            embedding = self.embed_caption(caption)
            yield embedding

    async def embed_caption_stream_async(
        self, caption_stream, embed_final_only: bool = True
    ):

        async for caption in caption_stream:
            if embed_final_only and not caption.get("is_final", False):
                continue

            transcript = caption.get("transcript", "")
            if not transcript.strip():
                continue

            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(None, self.embed_caption, caption)

            yield embedding

    def search_similar(
        self, query: str, k: int = 5, threshold: float = 0.7
    ) -> List[Dict[str, Any]]:

        query_embedding = self.model.encode(query, convert_to_numpy=True)
        query_embedding = query_embedding.reshape(1, -1).astype("float32")

        distances, indices = self.embeddings_index.search(query_embedding, k)

        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < 0 or idx >= len(self.caption_store):
                continue

            similarity = 1.0 / (1.0 + distance)

            if similarity >= threshold:
                caption_embedding = self.caption_store[idx]

                results.append(
                    {
                        "rank": i + 1,
                        "similarity": float(similarity),
                        "distance": float(distance),
                        "caption": caption_embedding.caption,
                        "timestamp": caption_embedding.timestamp,
                        "metadata": caption_embedding.metadata,
                    }
                )

        return results

    def search_by_semantic_similarity(
        self, query_caption: Dict[str, Any], k: int = 5
    ) -> List[Dict[str, Any]]:

        query_text = query_caption.get("transcript", "")
        return self.search_similar(query_text, k)

    def cluster_captions(
        self, n_clusters: int = 5, method: str = "kmeans"
    ) -> Dict[str, Any]:

        if len(self.caption_store) < n_clusters:
            return {
                "error": f"Not enough captions for {n_clusters} clusters. Have {len(self.caption_store)}, need at least {n_clusters}.",
                "n_captions": len(self.caption_store),
            }

        embeddings = np.array([ce.embedding for ce in self.caption_store]).astype(
            "float32"
        )

        if method == "kmeans":
            kmeans = faiss.Kmeans(
                self.embedding_dim, n_clusters, niter=20, verbose=False
            )
            kmeans.train(embeddings)

            _, cluster_ids = kmeans.index.search(embeddings, 1)
            cluster_ids = cluster_ids.flatten()
        else:
            return {"error": f"Unsupported clustering method: {method}"}

        clusters = {}
        for idx, caption_embedding in enumerate(self.caption_store):
            cluster_id = int(cluster_ids[idx])

            if cluster_id not in clusters:
                clusters[cluster_id] = {"captions": [], "centroid": None, "size": 0}

            clusters[cluster_id]["captions"].append(caption_embedding)
            clusters[cluster_id]["size"] += 1

        if method == "kmeans":
            for cluster_id in clusters:
                clusters[cluster_id]["centroid"] = kmeans.centroids[cluster_id].tolist()

        cluster_summaries = {}
        for cluster_id, cluster_data in clusters.items():
            sample_captions = [
                ce.caption.get("transcript", "")[:50]
                for ce in cluster_data["captions"][:3]
            ]
            cluster_summaries[cluster_id] = {
                "size": cluster_data["size"],
                "sample_captions": sample_captions,
                "centroid": cluster_data.get("centroid"),
            }

        return {
            "n_clusters": n_clusters,
            "total_captions": len(self.caption_store),
            "clusters": clusters,
            "cluster_summaries": cluster_summaries,
            "method": method,
        }

    def save_index(self, filepath: str):
        import pickle

        data = {
            "model_name": self.model_name,
            "embedding_dim": self.embedding_dim,
            "caption_store": [ce.to_dict() for ce in self.caption_store],
            "faiss_index": faiss.serialize_index(self.embeddings_index),
        }

        with open(filepath, "wb") as f:
            pickle.dump(data, f)

    def load_index(self, filepath: str):
        import pickle

        with open(filepath, "rb") as f:
            data = pickle.load(f)

        self.model_name = data["model_name"]
        self.embedding_dim = data["embedding_dim"]
        self.caption_store = [
            CaptionEmbedding.from_dict(ce_dict) for ce_dict in data["caption_store"]
        ]
        self.embeddings_index = faiss.deserialize_index(data["faiss_index"])

    def get_statistics(self) -> Dict[str, Any]:
        total_captions = len(self.caption_store)

        if total_captions == 0:
            return {
                "total_captions": 0,
                "embedding_dim": self.embedding_dim,
                "model_name": self.model_name,
            }

        final_captions = [
            ce for ce in self.caption_store if ce.caption.get("is_final", False)
        ]
        languages = {}
        speakers = {}

        for ce in self.caption_store:
            lang = ce.metadata.get("language_code", "unknown")
            languages[lang] = languages.get(lang, 0) + 1

            speaker = ce.metadata.get("speaker_tag", "unknown")
            speakers[speaker] = speakers.get(speaker, 0) + 1

        embeddings = np.array([ce.embedding for ce in self.caption_store])
        embedding_norms = np.linalg.norm(embeddings, axis=1)

        return {
            "total_captions": total_captions,
            "final_captions": len(final_captions),
            "embedding_dim": self.embedding_dim,
            "model_name": self.model_name,
            "language_distribution": languages,
            "speaker_distribution": speakers,
            "embedding_stats": {
                "mean_norm": float(np.mean(embedding_norms)),
                "std_norm": float(np.std(embedding_norms)),
                "min_norm": float(np.min(embedding_norms)),
                "max_norm": float(np.max(embedding_norms)),
            },
        }


class MeetingSemanticSearch:
    def __init__(self, embedder: CaptionEmbedder):
        self.embedder = embedder

    def search_meeting_content(
        self, query: str, filters: Optional[Dict[str, Any]] = None, k: int = 10
    ) -> Dict[str, Any]:

        semantic_results = self.embedder.search_similar(query, k=k * 2)

        if filters:
            filtered_results = []
            for result in semantic_results:
                caption = result["caption"]
                metadata = result.get("metadata", {})

                matches = True
                for key, value in filters.items():
                    if key == "speaker":
                        if metadata.get("speaker_tag") != value:
                            matches = False
                            break
                    elif key == "language":
                        if metadata.get("language_code") != value:
                            matches = False
                            break
                    elif key == "time_range":
                        start, end = value
                        timestamp = result.get("timestamp")
                        if timestamp and not (start <= timestamp <= end):
                            matches = False
                            break
                    elif key == "min_confidence":
                        if metadata.get("confidence", 0) < value:
                            matches = False
                            break

                if matches:
                    filtered_results.append(result)

            semantic_results = filtered_results[:k]
        else:
            semantic_results = semantic_results[:k]

        topics = self._extract_topics(semantic_results)

        return {
            "query": query,
            "results": semantic_results,
            "total_found": len(semantic_results),
            "topics": topics,
            "filters_applied": filters is not None,
        }

    def _extract_topics(self, results: List[Dict[str, Any]]) -> List[str]:
        if not results:
            return []

        captions = [r["caption"].get("transcript", "") for r in results[:5]]

        common_words = {}
        for caption in captions:
            words = caption.lower().split()
            for word in words:
                if len(word) > 3 and word not in [
                    "that",
                    "this",
                    "with",
                    "from",
                    "have",
                    "were",
                    "they",
                ]:
                    common_words[word] = common_words.get(word, 0) + 1

        sorted_words = sorted(common_words.items(), key=lambda x: x[1], reverse=True)
        topics = [word for word, count in sorted_words[:5] if count > 1]

        return topics


def example_caption_stream():
    captions = [
        {
            "transcript": "We need to improve our API response times.",
            "is_final": True,
            "language_code": "en",
            "speaker_tag": 1,
        },
        {
            "transcript": "The database queries are taking too long.",
            "is_final": True,
            "language_code": "en",
            "speaker_tag": 2,
        },
        {
            "transcript": "Let's implement caching for frequent requests.",
            "is_final": True,
            "language_code": "en",
            "speaker_tag": 1,
        },
        {
            "transcript": "Marketing campaign results look promising.",
            "is_final": True,
            "language_code": "en",
            "speaker_tag": 3,
        },
        {
            "transcript": "User engagement has increased by 20%.",
            "is_final": True,
            "language_code": "en",
            "speaker_tag": 3,
        },
        {
            "transcript": "We should focus on mobile optimization next.",
            "is_final": True,
            "language_code": "en",
            "speaker_tag": 2,
        },
    ]

    for caption in captions:
        yield caption


if __name__ == "__main__":
    embedder = CaptionEmbedder(model_name="all-MiniLM-L6-v2")

    caption_gen = example_caption_stream()

    print("Generating caption embeddings...")
    embeddings = []

    for embedding in embedder.embed_caption_stream(caption_gen):
        embeddings.append(embedding)
        print(f"Embedded: {embedding.caption['transcript'][:50]}...")

    print(f"\nTotal embeddings: {len(embeddings)}")

    print("\nSearching for similar content to 'API performance':")
    results = embedder.search_similar("API performance", k=3)

    for result in results:
        print(f"Similarity: {result['similarity']:.3f}")
        print(f"Caption: {result['caption']['transcript']}")
        print("-" * 40)

    stats = embedder.get_statistics()
    print(f"\nEmbedding statistics:")
    print(f"Model: {stats['model_name']}")
    print(f"Dimensions: {stats['embedding_dim']}")
    print(f"Total captions: {stats['total_captions']}")
