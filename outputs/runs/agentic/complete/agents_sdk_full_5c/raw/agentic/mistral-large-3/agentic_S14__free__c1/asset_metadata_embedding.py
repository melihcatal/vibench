from google.cloud import aiplatform
from google.cloud.aiplatform import gapic
from storage_client import get_storage_client, get_bucket_name
from storage_models import ObjectMetadata
import json


def embed_asset_metadata(object_name: str, extracted_text: str) -> list[float]:
    """
    Embed object metadata and extracted text for search using Google Cloud Vertex AI.
    
    Args:
        object_name: Name of the object in the bucket.
        extracted_text: Text extracted from the object (e.g., via OCR).
        
    Returns:
        Embedding vector as a list of floats.
    """
    # Fetch object metadata
    bucket_name = get_bucket_name()
    bucket = get_storage_client().bucket(bucket_name)
    blob = bucket.blob(object_name)
    blob.reload()
    
    metadata: ObjectMetadata = {
        "name": blob.name,
        "size": blob.size,
        "content_type": blob.content_type,
        "time_created": blob.time_created.isoformat(),
        "updated": blob.updated.isoformat(),
        "md5_hash": blob.md5_hash,
        "metadata": blob.metadata or {}
    }
    
    # Combine metadata and extracted text
    combined_text = (
        f"Metadata: {json.dumps(metadata)} "
        f"Content: {extracted_text}"
    )
    
    # Generate embedding using Vertex AI text embedding model
    client = gapic.PredictionServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )
    endpoint = f"projects/{aiplatform.project}/locations/us-central1/publishers/google/models/textembedding-gecko"
    
    instance = {"content": combined_text}
    instances = [instance]
    
    response = client.predict(
        endpoint=endpoint,
        instances=instances
    )
    
    return response.predictions[0]["embeddings"]["values"]