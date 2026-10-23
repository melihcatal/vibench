import os
from google.cloud import aiplatform

def embed_output(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = config.get('location') or os.environ.get('GOOGLE_CLOUD_REGION', 'us-central1')

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.Preview.models.TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    response = model.predict([payload['text']])
    
    # The response contains a list of embeddings. For a single text input, we take the first one.
    embeddings = [embedding.values for embedding in response[0].embeddings]

    return {'embedding': embeddings[0]}
