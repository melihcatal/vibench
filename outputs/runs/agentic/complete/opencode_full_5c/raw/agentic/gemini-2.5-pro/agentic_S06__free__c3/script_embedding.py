from google.cloud import aiplatform
from speech_client import get_project_id
from speech_models import EmbeddingRequest


def embed_script(request: EmbeddingRequest) -> list[float]:
    """Generates embeddings for a narration script."""
    project_id = get_project_id()
    location = "us-central1"  # Or your preferred location

    aiplatform.init(project=project_id, location=location)

    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    )

    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/text-embedding-004"

    instance = {"content": request.script_content}

    response = client.predict(endpoint=endpoint, instances=[instance])

    # Assuming one instance in, one prediction out
    embedding = response.predictions[0]["embeddings"]["values"]
    return embedding
