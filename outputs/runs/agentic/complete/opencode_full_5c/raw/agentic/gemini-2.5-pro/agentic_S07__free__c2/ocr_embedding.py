from typing import List
from google.cloud import aiplatform


def get_text_embedding(text: str, project_id: str, location: str) -> List[float]:
    """
    Generates a text embedding for a given text using Google Cloud Vertex AI.
    """
    aiplatform.init(project=project_id, location=location)

    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )

    endpoint = (
        f"projects/{project_id}/locations/{location}/"
        "publishers/google/models/text-embedding-004"
    )

    instance = {"content": text}

    response = client.predict(endpoint=endpoint, instances=[instance])

    embedding = response.predictions[0]["embedding"]
    return embedding
