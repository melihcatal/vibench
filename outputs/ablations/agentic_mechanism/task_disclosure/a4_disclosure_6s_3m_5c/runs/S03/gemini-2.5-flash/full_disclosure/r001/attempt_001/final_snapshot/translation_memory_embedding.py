from typing import List

from google.cloud import aiplatform
from google.api_core.client_options import ClientOptions

def embed_translated_segments(
    project_id: str,
    location: str,
    segments: List[str]
) -> List[List[float]]:
    client_options = ClientOptions(api_endpoint=f"{location}-aiplatform.googleapis.com")
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/text-embedding-004"

    instances = [{"content": segment} for segment in segments]
    
    response = client.predict(endpoint=endpoint, instances=instances)
    
    embeddings = []
    for prediction in response.predictions:
        embeddings.append(prediction["embeddings"]["values"])
        
    return embeddings
