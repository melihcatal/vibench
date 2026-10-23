import json
from typing import Dict, List

from google.cloud import aiplatform
from google.cloud.aiplatform import gapic


def embed_metadata_and_text(metadata: Dict[str, str], text: str) -> List[float]:
    """
    Embed object metadata and extracted text for search using Google Cloud Vertex AI.
    
    Args:
        metadata: Dictionary of object metadata.
        text: Extracted text from the object.
        
    Returns:
        Embedding vector as a list of floats.
    """
    client = gapic.PredictionServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )

    endpoint = f"projects/{aiplatform.project}/locations/us-central1/publishers/google/models/multimodalembedding@001"

    combined_input = json.dumps({
        "metadata": metadata,
        "text": text
    })

    instance = {"text": combined_input}
    instances = [instance]

    response = client.predict(
        endpoint=endpoint,
        instances=instances
    )

    return response.predictions[0]["textEmbedding"]