import os
import asyncio
from typing import AsyncGenerator, Dict, Any, List, Optional
import numpy as np
from openai import OpenAI


class CaptionEmbedder:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable must be set")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

        self.available_models = {
            "text-embedding-3-large": "OpenAI Embedding 3 Large (3072 dimensions)",
            "text-embedding-3-small": "OpenAI Embedding 3 Small (1536 dimensions)",
            "text-embedding-ada-002": "OpenAI Ada Embedding v2 (1536 dimensions)",
            "text-embedding-3-large-256": "OpenAI Embedding 3 Large truncated to 256 dimensions",
            "text-embedding-3-small-512": "OpenAI Embedding 3 Small truncated to 512 dimensions",
        }

    async def embed_caption(
        self, caption_text: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        if not caption_text.strip():
            return {
                "text": caption_text,
                "embedding": [],
                "dimensions": 0,
                "model": self.model,
                "metadata": metadata or {},
            }

        try:
            response = self.client.embeddings.create(
                model=self.model, input=caption_text, encoding_format="float"
            )

            embedding = response.data[0].embedding

            return {
                "text": caption_text,
                "embedding": embedding,
                "dimensions": len(embedding),
                "model": self.model,
                "metadata": metadata or {},
                "provider": "OpenAI",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
            }

        except Exception as e:
            return {
                "text": caption_text,
                "embedding": [],
                "dimensions": 0,
                "model": self.model,
                "metadata": metadata or {},
                "error": str(e),
                "provider": "OpenAI",
            }

    async def stream_embed_captions(
        self, caption_stream: AsyncGenerator[Dict[str, Any], None]
    ) -> AsyncGenerator[Dict[str, Any], None]:
        async for caption in caption_stream:
            caption_text = caption.get("text", "")
            is_final = caption.get("is_final", True)

            metadata = {
                "is_final": is_final,
                "timestamp": caption.get("timestamp"),
                "language": caption.get("language", "en-US"),
                "confidence": caption.get("confidence", 0.0),
            }

            embedding_result = await self.embed_caption(caption_text, metadata)

            result = {
                **caption,
                "embedding": embedding_result,
                "vector": embedding_result["embedding"],
                "embedding_metadata": {
                    "model": embedding_result["model"],
                    "dimensions": embedding_result["dimensions"],
                    "provider": "OpenAI",
                },
            }

            yield result

    async def batch_embed_captions(
        self, captions: List[str], batch_size: int = 10
    ) -> List[Dict[str, Any]]:
        results = []

        for i in range(0, len(captions), batch_size):
            batch = captions[i : i + batch_size]

            try:
                response = self.client.embeddings.create(
                    model=self.model, input=batch, encoding_format="float"
                )

                for j, data in enumerate(response.data):
                    if i + j < len(captions):
                        results.append(
                            {
                                "text": captions[i + j],
                                "embedding": data.embedding,
                                "dimensions": len(data.embedding),
                                "model": self.model,
                                "provider": "OpenAI",
                                "index": data.index,
                            }
                        )

            except Exception as e:
                for j in range(len(batch)):
                    results.append(
                        {
                            "text": batch[j],
                            "embedding": [],
                            "dimensions": 0,
                            "model": self.model,
                            "error": str(e),
                            "provider": "OpenAI",
                        }
                    )

            await asyncio.sleep(0.1)

        return results

    def set_model(self, model_name: str):
        if model_name not in self.available_models:
            raise ValueError(
                f"Unsupported model: {model_name}. Available: {list(self.available_models.keys())}"
            )
        self.model = model_name


class SemanticSearchIndex:
    def __init__(self, embedder: CaptionEmbedder):
        self.embedder = embedder
        self.index = []
        self.texts = []
        self.metadata = []

    async def add_caption(self, caption: Dict[str, Any]):
        embedding_result = await self.embedder.embed_caption(
            caption.get("text", ""),
            {
                "timestamp": caption.get("timestamp"),
                "is_final": caption.get("is_final", True),
                "original_data": caption,
            },
        )

        if embedding_result["embedding"]:
            self.index.append(embedding_result["embedding"])
            self.texts.append(caption.get("text", ""))
            self.metadata.append(embedding_result["metadata"])

    async def search_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = await self.embedder.embed_caption(query)

        if not query_embedding["embedding"]:
            return []

        query_vec = np.array(query_embedding["embedding"])

        if not self.index:
            return []

        similarities = []
        for i, vec in enumerate(self.index):
            if vec:
                vec_array = np.array(vec)
                similarity = np.dot(query_vec, vec_array) / (
                    np.linalg.norm(query_vec) * np.linalg.norm(vec_array)
                )
                similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for i, (idx, similarity) in enumerate(similarities[:top_k]):
            results.append(
                {
                    "rank": i + 1,
                    "text": self.texts[idx],
                    "similarity": float(similarity),
                    "metadata": self.metadata[idx],
                    "index": idx,
                }
            )

        return results

    async def find_semantic_clusters(
        self, threshold: float = 0.8
    ) -> List[List[Dict[str, Any]]]:
        if not self.index:
            return []

        vectors = [np.array(vec) for vec in self.index if vec]
        texts = [text for text, vec in zip(self.texts, self.index) if vec]
        metadata_list = [meta for meta, vec in zip(self.metadata, self.index) if vec]

        clusters = []
        visited = set()

        for i in range(len(vectors)):
            if i in visited:
                continue

            cluster = [{"text": texts[i], "metadata": metadata_list[i], "index": i}]
            visited.add(i)

            for j in range(i + 1, len(vectors)):
                if j in visited:
                    continue

                similarity = np.dot(vectors[i], vectors[j]) / (
                    np.linalg.norm(vectors[i]) * np.linalg.norm(vectors[j])
                )
                if similarity >= threshold:
                    cluster.append(
                        {
                            "text": texts[j],
                            "metadata": metadata_list[j],
                            "index": j,
                            "similarity_to_center": float(similarity),
                        }
                    )
                    visited.add(j)

            if len(cluster) > 1:
                clusters.append(cluster)

        return clusters

    def get_index_stats(self) -> Dict[str, Any]:
        return {
            "total_captions": len(self.texts),
            "total_embeddings": len([v for v in self.index if v]),
            "average_text_length": sum(len(t) for t in self.texts) / len(self.texts)
            if self.texts
            else 0,
            "dimensions": len(self.index[0]) if self.index and self.index[0] else 0,
        }


async def embed_live_captions(
    caption_stream: AsyncGenerator[Dict[str, Any], None],
    model: str = "text-embedding-3-small",
    build_index: bool = False,
) -> AsyncGenerator[Dict[str, Any], None]:
    embedder = CaptionEmbedder(model=model)

    if build_index:
        index = SemanticSearchIndex(embedder)

        async for caption in caption_stream:
            await index.add_caption(caption)

            embedding_result = await embedder.embed_caption(
                caption.get("text", ""),
                {
                    "timestamp": caption.get("timestamp"),
                    "is_final": caption.get("is_final", True),
                },
            )

            yield {
                **caption,
                "embedding": embedding_result,
                "index_stats": index.get_index_stats(),
            }

        yield {
            "type": "index_complete",
            "index_stats": index.get_index_stats(),
            "total_captions": len(index.texts),
        }
    else:
        async for embedded in embedder.stream_embed_captions(caption_stream):
            yield embedded


class MeetingTopicAnalyzer:
    def __init__(self, embedder: CaptionEmbedder):
        self.embedder = embedder
        self.topic_embeddings = {}

    async def identify_topics(
        self, captions: List[Dict[str, Any]], num_topics: int = 5
    ) -> List[Dict[str, Any]]:
        if not captions:
            return []

        texts = [c.get("text", "") for c in captions]
        embeddings = await self.embedder.batch_embed_captions(texts)

        valid_embeddings = [e for e in embeddings if e.get("embedding")]
        if not valid_embeddings:
            return []

        vectors = np.array([e["embedding"] for e in valid_embeddings])

        from sklearn.cluster import KMeans

        kmeans = KMeans(n_clusters=min(num_topics, len(vectors)), random_state=42)
        clusters = kmeans.fit_predict(vectors)

        topics = []
        for cluster_id in range(kmeans.n_clusters):
            cluster_indices = np.where(clusters == cluster_id)[0]
            cluster_texts = [texts[i] for i in cluster_indices if i < len(texts)]

            if cluster_texts:
                centroid = kmeans.cluster_centers_[cluster_id]

                representative_idx = np.argmin(
                    [np.linalg.norm(vec - centroid) for vec in vectors[cluster_indices]]
                )
                representative_text = (
                    cluster_texts[representative_idx]
                    if representative_idx < len(cluster_texts)
                    else ""
                )

                topics.append(
                    {
                        "topic_id": cluster_id,
                        "representative_text": representative_text,
                        "caption_count": len(cluster_texts),
                        "captions": cluster_texts[:5],
                        "centroid": centroid.tolist(),
                    }
                )

        return topics


if __name__ == "__main__":

    async def mock_caption_stream():
        captions = [
            {
                "text": "We need to improve our customer service response times",
                "is_final": True,
            },
            {
                "text": "The new software update will be released next week",
                "is_final": True,
            },
            {
                "text": "Customer feedback has been positive about the new features",
                "is_final": True,
            },
            {
                "text": "We should schedule training for the support team",
                "is_final": True,
            },
            {
                "text": "The update includes performance improvements and bug fixes",
                "is_final": True,
            },
        ]

        for caption in captions:
            yield caption
            await asyncio.sleep(0.3)

    async def main():
        embedder = CaptionEmbedder()

        async for embedded in embedder.stream_embed_captions(mock_caption_stream()):
            print(f"Caption: {embedded.get('text')}")
            print(
                f"Embedding dimensions: {embedded.get('embedding_metadata', {}).get('dimensions')}"
            )
            print(f"Model: {embedded.get('embedding_metadata', {}).get('model')}")
            print("---")

    asyncio.run(main())
