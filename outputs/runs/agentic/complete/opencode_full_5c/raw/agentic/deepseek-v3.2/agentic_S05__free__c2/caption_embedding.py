from google.cloud import aiplatform
from typing import List, Dict, Any, Generator
import numpy as np
from dataclasses import dataclass
import time


@dataclass
class CaptionEmbedding:
    text: str
    embedding: List[float]
    timestamp: float
    is_final: bool
    metadata: Dict[str, Any]


class CaptionEmbedder:
    def __init__(self, project_id: str = None, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.endpoint = "textembedding-gecko@001"

        aiplatform.init(project=project_id, location=location)

    def get_embedding(self, text: str) -> List[float]:
        from google.cloud import aiplatform_v1beta1

        client = aiplatform_v1beta1.PredictionServiceClient(
            client_options={
                "api_endpoint": f"{self.location}-aiplatform.googleapis.com"
            }
        )

        instance = {"content": text}
        instances = [instance]

        endpoint = client.endpoint_path(
            project=self.project_id,
            location=self.location,
            endpoint=self.endpoint,
        )

        try:
            response = client.predict(
                endpoint=endpoint,
                instances=instances,
            )

            if response.predictions and len(response.predictions) > 0:
                embedding = (
                    response.predictions[0].get("embeddings", {}).get("values", [])
                )
                if embedding:
                    return embedding

            return []

        except Exception as e:
            print(f"Embedding error: {e}")
            return []

    def batch_embed(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            embedding = self.get_embedding(text)
            embeddings.append(embedding)
        return embeddings

    def semantic_similarity(
        self, embedding1: List[float], embedding2: List[float]
    ) -> float:
        if not embedding1 or not embedding2:
            return 0.0

        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return np.dot(vec1, vec2) / (norm1 * norm2)

    def search_similar(
        self,
        query_embedding: List[float],
        caption_embeddings: List[CaptionEmbedding],
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        similarities = []

        for caption in caption_embeddings:
            similarity = self.semantic_similarity(query_embedding, caption.embedding)
            similarities.append(
                {
                    "caption": caption.text,
                    "similarity": similarity,
                    "timestamp": caption.timestamp,
                    "metadata": caption.metadata,
                }
            )

        return sorted(similarities, key=lambda x: x["similarity"], reverse=True)[:top_k]

    def embed_caption_stream(
        self, caption_stream: Generator[Dict[str, Any], None, None]
    ) -> Generator[CaptionEmbedding, None, None]:
        for caption in caption_stream:
            if caption.get("is_final", False):
                transcript = caption.get("transcript", "")

                if transcript.strip():
                    embedding = self.get_embedding(transcript)

                    caption_embedding = CaptionEmbedding(
                        text=transcript,
                        embedding=embedding,
                        timestamp=time.time(),
                        is_final=True,
                        metadata={
                            "confidence": caption.get("confidence"),
                            "language": caption.get("language", "en"),
                            "source": "speech_to_text",
                        },
                    )

                    yield caption_embedding
            else:
                yield CaptionEmbedding(
                    text=caption.get("transcript", ""),
                    embedding=[],
                    timestamp=time.time(),
                    is_final=False,
                    metadata={"type": "partial"},
                )

    def create_semantic_index(
        self, caption_embeddings: List[CaptionEmbedding]
    ) -> Dict[str, Any]:
        if not caption_embeddings:
            return {"total_embeddings": 0, "average_dimensions": 0}

        valid_embeddings = [e for e in caption_embeddings if e.embedding]

        if not valid_embeddings:
            return {"total_embeddings": 0, "average_dimensions": 0}

        dimensions = len(valid_embeddings[0].embedding)
        total_text_length = sum(len(e.text.split()) for e in valid_embeddings)

        return {
            "total_embeddings": len(valid_embeddings),
            "average_dimensions": dimensions,
            "total_text_length": total_text_length,
            "embedding_model": self.endpoint,
            "timestamp": time.time(),
        }


def embed_caption_chunks(caption_stream, project_id=None):
    embedder = CaptionEmbedder(project_id=project_id)

    all_embeddings = []

    for embedding in embedder.embed_caption_stream(caption_stream):
        if embedding.embedding:
            print(
                f"Embedded: {embedding.text[:50]}... (dims: {len(embedding.embedding)})"
            )
            all_embeddings.append(embedding)

        yield embedding

    if all_embeddings:
        index_info = embedder.create_semantic_index(all_embeddings)
        print(f"\nSemantic index created: {index_info}")

        if len(all_embeddings) >= 2:
            query = "meeting discussion"
            query_embedding = embedder.get_embedding(query)

            if query_embedding:
                similar = embedder.search_similar(
                    query_embedding, all_embeddings, top_k=3
                )
                print(f"\nSimilar to '{query}':")
                for item in similar:
                    print(
                        f"  - {item['caption'][:60]}... (similarity: {item['similarity']:.3f})"
                    )


if __name__ == "__main__":
    test_captions = [
        {
            "transcript": "We discussed the project timeline and deliverables",
            "is_final": True,
        },
        {"transcript": "The team agreed on using agile methodology", "is_final": True},
        {"transcript": "Budget needs to be approved by next week", "is_final": True},
    ]

    for embedding in embed_caption_chunks(test_captions):
        print(embedding)
