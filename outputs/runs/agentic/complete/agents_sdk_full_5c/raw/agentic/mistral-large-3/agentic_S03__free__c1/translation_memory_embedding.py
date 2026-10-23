import os
from typing import List
from google.cloud import aiplatform
from translation_models import TranslationRequest

def translation_memory_embedding(text: str, model: str = "textembedding-gecko") -> List[float]:
    """Embed translated segments for translation-memory search using Vertex AI."""
    client = aiplatform.gapic.PredictionServiceClient(
        client_options={"api_endpoint": f"us-central1-aiplatform.googleapis.com"}
    )
    endpoint = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/us-central1/publishers/google/models/{model}"
    
    response = client.predict(
        endpoint=endpoint,
        instances=[{"content": text}],
        parameters={},
    )
    
    return response.predictions[0]["embeddings"]["values"]