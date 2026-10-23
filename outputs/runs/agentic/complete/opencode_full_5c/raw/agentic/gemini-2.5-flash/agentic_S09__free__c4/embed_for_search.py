import os
from typing import List, Dict
from google.cloud import aiplatform
from embeddings_client import EmbeddingsClient
from embeddings_models import TextEmbeddingResponse


class SearchEmbeddingsClient(EmbeddingsClient):
    def embed_query(self, query: str) -> TextEmbeddingResponse:
        instances = [
            {
                "content": query,
                "task_type": "RETRIEVAL_QUERY",
                "title": "",
                "query_type": "",
            }
        ]
        endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_name}"
        response = self.client.predict(endpoint=endpoint, instances=instances)
        embedding = response.predictions[0]["embeddings"]["values"]
        return TextEmbeddingResponse(embedding=embedding)

    def embed_documents(self, documents: List[str]) -> List[TextEmbeddingResponse]:
        instances = []
        for doc in documents:
            instances.append(
                {
                    "content": doc,
                    "task_type": "RETRIEVAL_DOCUMENT",
                    "title": "",
                    "query_type": "",
                }
            )
        endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model_name}"
        response = self.client.predict(endpoint=endpoint, instances=instances)
        embeddings = [
            prediction["embeddings"]["values"] for prediction in response.predictions
        ]
        return [TextEmbeddingResponse(embedding=e) for e in embeddings]


def embed_for_semantic_search(
    query: str, documents: List[str]
) -> Dict[str, List[List[float]]]:
    """Embeds a query and documents for semantic search using Vertex AI."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = SearchEmbeddingsClient(project_id=project_id, location=location)
    query_embedding = client.embed_query(query).embedding
    document_embeddings = [res.embedding for res in client.embed_documents(documents)]

    return {
        "query_embedding": query_embedding,
        "document_embeddings": document_embeddings,
    }
