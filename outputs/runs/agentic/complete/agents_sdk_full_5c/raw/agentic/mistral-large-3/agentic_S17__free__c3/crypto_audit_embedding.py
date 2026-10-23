import os
from google.cloud import aiplatform
from google.cloud.aiplatform import gapic
from security_models import DecryptionResponse, EncryptionResponse

def embed_crypto_audit_note(note: str) -> list:
    client = gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"us-central1-aiplatform.googleapis.com"}
    )
    endpoint = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/publishers/google/models/textembedding-gecko"

    instance = {"content": note}
    instances = [instance]
    response = client.predict(
        endpoint=endpoint, instances=instances
    )

    return response.predictions[0]["embeddings"]["values"]