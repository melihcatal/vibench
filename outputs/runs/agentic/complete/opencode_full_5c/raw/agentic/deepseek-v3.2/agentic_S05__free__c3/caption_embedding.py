from google.cloud import aiplatform
from typing import Generator, Dict, Any, List, Optional
import numpy as np
from datetime import datetime
import asyncio


class CaptionEmbedder:
    def __init__(self, project_id: Optional[str] = None, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.endpoint_id = "textembedding-gecko"
        self.model_id = "textembedding-gecko@001"

        aiplatform.init(project=project_id, location=location)

        self.embeddings = []
        self.caption_metadata = []

    def get_embedding(self, text: str) -> np.ndarray:
        if not text.strip():
            return np.zeros(768)

        try:
            from google.cloud import aiplatform_v1
            from google.protobuf import struct_pb2

            client = aiplatform_v1.PredictionServiceClient(
                client_options={
                    "api_endpoint": f"{self.location}-aiplatform.googleapis.com"
                }
            )

            instance = struct_pb2.Struct()
            instance.fields["content"].string_value = text

            instances = [instance]

            endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_id}"

            response = client.predict(endpoint=endpoint, instances=instances)

            if response.predictions:
                prediction = response.predictions[0]
                if "embeddings" in prediction:
                    embeddings_dict = prediction["embeddings"]
                    if "values" in embeddings_dict:
                        values = embeddings_dict["values"]
                        return np.array(values, dtype=np.float32)

            return np.zeros(768)

        except Exception as e:
            print(f"Embedding generation error: {e}")
            return np.zeros(768)

    async def get_embedding_async(self, text: str) -> np.ndarray:
        return await asyncio.to_thread(self.get_embedding, text)

    def embed_caption(self, caption: Dict[str, Any]) -> Dict[str, Any]:
        transcript = caption.get("transcript", "")
        is_final = caption.get("is_final", False)

        embedding = self.get_embedding(transcript)

        embedded_caption = caption.copy()
        embedded_caption["embedding"] = embedding.tolist()
        embedded_caption["embedding_dim"] = len(embedding)
        embedded_caption["embedding_model"] = self.model_id
        embedded_caption["has_embedding"] = True

        if is_final:
            self.embeddings.append(embedding)
            self.caption_metadata.append(
                {
                    "transcript": transcript,
                    "timestamp": datetime.now().isoformat(),
                    "embedding": embedding.tolist(),
                }
            )

        return embedded_caption

    async def embed_caption_async(self, caption: Dict[str, Any]) -> Dict[str, Any]:
        transcript = caption.get("transcript", "")
        is_final = caption.get("is_final", False)

        embedding = await self.get_embedding_async(transcript)

        embedded_caption = caption.copy()
        embedded_caption["embedding"] = embedding.tolist()
        embedded_caption["embedding_dim"] = len(embedding)
        embedded_caption["embedding_model"] = self.model_id
        embedded_caption["has_embedding"] = True

        if is_final:
            self.embeddings.append(embedding)
            self.caption_metadata.append(
                {
                    "transcript": transcript,
                    "timestamp": datetime.now().isoformat(),
                    "embedding": embedding.tolist(),
                }
            )

        return embedded_caption

    def embed_caption_stream(
        self, caption_stream: Generator[Dict[str, Any], None, None]
    ) -> Generator[Dict[str, Any], None, None]:
        for caption in caption_stream:
            yield self.embed_caption(caption)

    async def embed_caption_stream_async(
        self, caption_stream
    ) -> Generator[Dict[str, Any], None, None]:
        async for caption in caption_stream:
            embedded = await self.embed_caption_async(caption)
            yield embedded

    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.get_embedding(query)

        if not self.embeddings:
            return []

        similarities = []
        for i, embedding in enumerate(self.embeddings):
            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
            )
            similarities.append((i, similarity))

        similarities.sort(key=lambda x: x[1], reverse=True)

        results = []
        for idx, similarity in similarities[:top_k]:
            if idx < len(self.caption_metadata):
                metadata = self.caption_metadata[idx]
                results.append(
                    {
                        "transcript": metadata["transcript"],
                        "timestamp": metadata["timestamp"],
                        "similarity": float(similarity),
                        "embedding_index": idx,
                    }
                )

        return results

    def find_similar_captions(
        self, caption_text: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        return self.semantic_search(caption_text, top_k)

    def cluster_captions(self, n_clusters: int = 3) -> Dict[str, Any]:
        if len(self.embeddings) < n_clusters:
            return {"clusters": [], "error": "Not enough embeddings for clustering"}

        try:
            from sklearn.cluster import KMeans

            embeddings_array = np.array(self.embeddings)

            kmeans = KMeans(
                n_clusters=min(n_clusters, len(self.embeddings)), random_state=42
            )
            cluster_labels = kmeans.fit_predict(embeddings_array)

            clusters = []
            for cluster_id in range(n_clusters):
                cluster_indices = np.where(cluster_labels == cluster_id)[0]

                cluster_captions = []
                for idx in cluster_indices:
                    if idx < len(self.caption_metadata):
                        cluster_captions.append(
                            self.caption_metadata[idx]["transcript"]
                        )

                if cluster_captions:
                    clusters.append(
                        {
                            "cluster_id": int(cluster_id),
                            "size": len(cluster_indices),
                            "center": kmeans.cluster_centers_[cluster_id].tolist(),
                            "sample_captions": cluster_captions[:3],
                        }
                    )

            return {
                "clusters": clusters,
                "total_captions": len(self.embeddings),
                "cluster_labels": cluster_labels.tolist(),
            }
        except ImportError:
            return {
                "clusters": [],
                "error": "scikit-learn not available for clustering",
            }
        except Exception as e:
            return {"clusters": [], "error": str(e)}

    def get_embedding_stats(self) -> Dict[str, Any]:
        if not self.embeddings:
            return {"count": 0, "dimension": 0}

        embeddings_array = np.array(self.embeddings)

        return {
            "count": len(self.embeddings),
            "dimension": embeddings_array.shape[1],
            "mean_norm": float(np.mean(np.linalg.norm(embeddings_array, axis=1))),
            "std_norm": float(np.std(np.linalg.norm(embeddings_array, axis=1))),
            "total_captions": len(self.caption_metadata),
        }


def create_embedding_pipeline(
    caption_stream: Generator[Dict[str, Any], None, None],
    project_id: Optional[str] = None,
    location: str = "us-central1",
) -> Generator[Dict[str, Any], None, None]:

    embedder = CaptionEmbedder(project_id=project_id, location=location)
    return embedder.embed_caption_stream(caption_stream)


async def create_async_embedding_pipeline(
    caption_stream, project_id: Optional[str] = None, location: str = "us-central1"
):

    embedder = CaptionEmbedder(project_id=project_id, location=location)
    async for embedded in embedder.embed_caption_stream_async(caption_stream):
        yield embedded


def embed_caption_chunks(
    caption_stream: Generator[Dict[str, Any], None, None],
    project_id: Optional[str] = None,
) -> Generator[Dict[str, Any], None, None]:

    return create_embedding_pipeline(caption_stream, project_id)
