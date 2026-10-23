import os
from typing import List
from safety_client import safety_client
from safety_models import SafetyModels
from google.cloud import language_v1

def moderation_reason_embedding(reasons: List[str]) -> List[float]:
    """Embed moderation rationales using the Vertex AI Embeddings API (text embedding model)."""
    client = language_v1.EmbeddingServiceV1Client()
    # Vertex AI endpoint is identified by 'us-central1-aiplatform.googleapis.com'
    client.client_options = {'api_endpoint': 'us-central1-aiplatform.googleapis.com'}
    response = client.embed_content(request={
        'content': {
            'text_snippet': {'content': '\n'.join(reasons)},
            'mime_type': 'text/plain'
        },
        # model identifier for the text embedding model (e.g., textembedding-gecko@002)
        'model': 'projects/PROJECT_ID/locations/us-central1/publishers/google/models/textembedding-gecko@002'
    })
    embedding = response.embeddings[0].embedding_data.float32_token_embeddings
    return list(embedding)
