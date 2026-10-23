
from google.cloud import aiplatform_v1beta1 as aiplatform
from typing import List

def embed_caption_chunks(
    project_id: str,
    location: str,
    caption_chunks: List[str]
) -> List[List[float]]:
    client = aiplatform.PredictionServiceClient(client_options={"api_endpoint": f"{location}-aiplatform.googleapis.com"})
    model_name = "text-embedding-004"
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_name}"

    instances = [{"content": chunk} for chunk in caption_chunks]
    
    response = client.predict(
        endpoint=endpoint,
        instances=instances,
    )

    embeddings = []
    for prediction in response.predictions:
        embeddings.append(prediction["embeddings"]["values"])
    
    return embeddings

