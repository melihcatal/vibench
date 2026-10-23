import os
from google.cloud import aiplatform
from typing import List


def transcript_embedding(
    transcript_segments: List[str], model_id="textembedding-gecko@001"
):
    """Embed transcript segments for semantic retrieval using Google Cloud Vertex AI."""
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set"
        )

    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set")

    location = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")

    aiplatform.init(project=project_id, location=location)

    from google.cloud.aiplatform_v1beta1.types import PredictRequest
    from google.cloud.aiplatform_v1beta1.services.prediction_service import (
        PredictionServiceClient,
    )

    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    client = PredictionServiceClient()

    embeddings = []
    for segment in transcript_segments:
        request = PredictRequest(endpoint=endpoint, instances=[{"content": segment}])

        response = client.predict(request=request)

        if response.predictions and len(response.predictions) > 0:
            embedding = response.predictions[0].get("embeddings", {}).get("values", [])
            embeddings.append(
                {
                    "segment": segment,
                    "embedding": embedding,
                    "dimension": len(embedding),
                }
            )

    return embeddings
