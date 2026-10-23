import os
import asyncio
from typing import Dict, Any, List, Optional
import numpy as np
from deepgram import Deepgram
import openai


class CaptionEmbedder:
    def __init__(self):
        self.dg_client = Deepgram(os.getenv("DEEPGRAM_API_KEY"))

        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

        self.embeddings_cache = {}
        self.caption_history = []

    def embed_text(
        self, text: str, model: str = "text-embedding-3-small"
    ) -> Optional[np.ndarray]:
        if not text.strip():
            return None

        cache_key = f"{model}:{text}"
        if cache_key in self.embeddings_cache:
            return self.embeddings_cache[cache_key]

        try:
            response = openai.embeddings.create(
                model=model, input=text, encoding_format="float"
            )

            embedding = np.array(response.data[0].embedding, dtype=np.float32)
            self.embeddings_cache[cache_key] = embedding
            return embedding

        except Exception as e:
            print(f"Embedding error: {e}")
            return None

    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        if embedding1 is None or embedding2 is None:
            return 0.0

        norm1 = np.linalg.norm(embedding1)
        norm2 = np.linalg.norm(embedding2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return np.dot(embedding1, embedding2) / (norm1 * norm2)

    async def embed_caption_stream(
        self, audio_source, embed_every: int = 3
    ) -> AsyncGenerator[Dict[str, Any], None]:
        caption_count = 0

        async with self.dg_client.transcription.live(
            {
                "model": "nova-2",
                "interim_results": True,
                "smart_format": True,
                "encoding": "linear16",
                "sample_rate": 16000,
                "channels": 1,
            }
        ) as connection:

            async def send_audio():
                async for audio_chunk in audio_source:
                    await connection.send(audio_chunk)

            async def process_captions():
                nonlocal caption_count

                async for message in connection:
                    if "channel" in message:
                        for alternative in message["channel"]["alternatives"]:
                            if "transcript" in alternative:
                                transcript = alternative["transcript"]
                                if transcript and message.get("is_final", False):
                                    caption_count += 1
                                    self.caption_history.append(
                                        {
                                            "text": transcript,
                                            "is_final": True,
                                            "timestamp": message.get("start", 0),
                                        }
                                    )

                                    if caption_count % embed_every == 0:
                                        recent_captions = self.caption_history[
                                            -embed_every:
                                        ]
                                        combined_text = " ".join(
                                            [c["text"] for c in recent_captions]
                                        )

                                        embedding = self.embed_text(combined_text)

                                        if embedding is not None:
                                            yield {
                                                "captions": recent_captions,
                                                "combined_text": combined_text,
                                                "embedding": embedding.tolist(),
                                                "embedding_dim": len(embedding),
                                                "model": "text-embedding-3-small",
                                                "caption_count": caption_count,
                                            }

            send_task = asyncio.create_task(send_audio())

            try:
                async for result in process_captions():
                    yield result
            finally:
                send_task.cancel()
                try:
                    await send_task
                except asyncio.CancelledError:
                    pass

    def search_similar_captions(
        self, query: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embed_text(query)
        if query_embedding is None:
            return []

        similarities = []
        for i, caption in enumerate(self.caption_history):
            if caption["text"]:
                caption_embedding = self.embed_text(caption["text"])
                if caption_embedding is not None:
                    sim = self.similarity(query_embedding, caption_embedding)
                    similarities.append(
                        {
                            "index": i,
                            "caption": caption["text"],
                            "similarity": sim,
                            "timestamp": caption.get("timestamp", 0),
                        }
                    )

        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        return similarities[:top_k]

    def cluster_captions(self, n_clusters: int = 3) -> Dict[str, Any]:
        if len(self.caption_history) < n_clusters:
            return {"clusters": [], "error": "Not enough captions to cluster"}

        from sklearn.cluster import KMeans

        embeddings = []
        valid_indices = []

        for i, caption in enumerate(self.caption_history):
            if caption["text"]:
                embedding = self.embed_text(caption["text"])
                if embedding is not None:
                    embeddings.append(embedding)
                    valid_indices.append(i)

        if len(embeddings) < n_clusters:
            return {"clusters": [], "error": "Not enough valid embeddings"}

        embeddings_array = np.array(embeddings)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(embeddings_array)

        clusters = []
        for cluster_id in range(n_clusters):
            cluster_indices = [
                valid_indices[i]
                for i, label in enumerate(cluster_labels)
                if label == cluster_id
            ]
            cluster_captions = [
                self.caption_history[idx]["text"] for idx in cluster_indices
            ]

            if cluster_captions:
                centroid = kmeans.cluster_centers_[cluster_id]
                clusters.append(
                    {
                        "cluster_id": cluster_id,
                        "size": len(cluster_captions),
                        "sample_captions": cluster_captions[:3],
                        "centroid": centroid.tolist(),
                    }
                )

        return {
            "total_captions": len(self.caption_history),
            "clustered_captions": len(embeddings),
            "clusters": clusters,
            "cluster_centers": kmeans.cluster_centers_.tolist(),
        }


async def example_embedding_stream():
    embedder = CaptionEmbedder()

    class TestAudio:
        async def __aiter__(self):
            for i in range(15):
                yield b"\x00" * 1024
                await asyncio.sleep(0.1)

    audio_source = TestAudio()

    print("Streaming captions and generating embeddings...")

    async for result in embedder.embed_caption_stream(audio_source, embed_every=2):
        print(
            f"\n--- Embedding batch (captions {result['caption_count'] - 1}-{result['caption_count']}) ---"
        )
        print(f"Combined text: {result['combined_text'][:100]}...")
        print(f"Embedding dimension: {result['embedding_dim']}")
        print(f"First 5 values: {result['embedding'][:5]}")

    print(f"\nTotal captions collected: {len(embedder.caption_history)}")

    if embedder.caption_history:
        test_query = "discussion about project timeline"
        print(f"\nSearching for: '{test_query}'")

        results = embedder.search_similar_captions(test_query, top_k=3)
        if results:
            print("Most similar captions:")
            for i, res in enumerate(results, 1):
                print(f"{i}. Similarity: {res['similarity']:.3f}")
                print(f"   Caption: {res['caption'][:80]}...")

        print("\nClustering captions...")
        clusters = embedder.cluster_captions(n_clusters=2)
        if "clusters" in clusters and clusters["clusters"]:
            print(f"Found {len(clusters['clusters'])} clusters:")
            for cluster in clusters["clusters"]:
                print(f"Cluster {cluster['cluster_id']} ({cluster['size']} captions):")
                for caption in cluster["sample_captions"][:2]:
                    print(f"  - {caption[:60]}...")


if __name__ == "__main__":
    asyncio.run(example_embedding_stream())
