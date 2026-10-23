import os
from typing import List
from google.cloud import aiplatform
from google.protobuf import json_format
from google.cloud.aiplatform.gapic.schema import predict
from model_models import LLMResponse

# Initialize Vertex AI for embeddings
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

if not PROJECT_ID:
    raise ValueError(
        "GOOGLE_CLOUD_PROJECT environment variable not set for embeddings."
    )

aiplatform.init(project=PROJECT_ID, location=LOCATION)


class VertexAIEmbeddingsClient:
    def __init__(self, project_id: str, location: str):
        self.project_id = project_id
        self.location = location
        self.prediction_client = aiplatform.gapic.PredictionServiceClient(
            client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
        )
        self.embedding_model_name = (
            "textembedding-gecko@003"  # A common text embedding model
        )

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        endpoint = f"projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.embedding_model_name}"

        instances = [{"content": text} for text in texts]

        instances_proto = [
            json_format.ParseDict(instance, predict.Instance()._pb)
            for instance in instances
        ]

        response = self.prediction_client.predict(
            endpoint=endpoint,
            instances=instances_proto,
        )

        embeddings = []
        for prediction in response.predictions:
            embedding = json_format.MessageToDict(prediction)["embeddings"]["values"]
            embeddings.append(embedding)

        return embeddings


_embedding_client = VertexAIEmbeddingsClient(project_id=PROJECT_ID, location=LOCATION)


def embed_model_outputs(texts: List[str]) -> LLMResponse:
    """
    Embeds model outputs for clustering or retrieval using Google Cloud Vertex AI Embeddings.
    """
    embeddings = _embedding_client.get_embeddings(texts)

    # Store embeddings as a string representation in text field, or as part of metadata
    # For now, let's put them in metadata and a placeholder in text.
    return LLMResponse(
        text=f"Embeddings generated for {len(texts)} texts.",
        metadata={
            "embedding_provider": "google_vertex_ai",
            "model_name": _embedding_client.embedding_model_name,
            "embeddings": embeddings,
        },
    )
