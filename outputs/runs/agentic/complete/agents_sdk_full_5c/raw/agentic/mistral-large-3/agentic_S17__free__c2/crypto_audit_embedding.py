import os
from google.cloud import aiplatform
from typing import List, Dict

def embed_crypto_audit_notes(notes: List[str]) -> List[List[float]]:
    aiplatform.init(project=os.getenv("GCP_PROJECT_ID"), location=os.getenv("GCP_LOCATION_ID"))
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"{os.getenv('GCP_LOCATION_ID')}-aiplatform.googleapis.com"}
    )

    model_name = f"projects/{os.getenv('GCP_PROJECT_ID')}/locations/{os.getenv('GCP_LOCATION_ID')}/publishers/google/models/textembedding-gecko"

    instances = [{"content": note} for note in notes]
    response = client.predict(
        endpoint=model_name,
        instances=instances
    )

    return [prediction["embeddings"]["values"] for prediction in response.predictions]