from google.cloud import aiplatform
import os

def embed_translation_segment(payload, config=None):
    config = config or {}
    project_id = config.get('project_id') or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = config.get('location') or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1") # Default to us-central1
    model_name = config.get('model_name') or "text-embedding-004" # A common text embedding model

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set as GOOGLE_CLOUD_PROJECT environment variable.")

    aiplatform.init(project=project_id, location=location)

    # Initialize the Vertex AI Embedding Model client
    # Using a pre-trained model for text embeddings
    # The specific model name might vary, check Vertex AI documentation for available models.
    model = aiplatform.models.TextEmbeddingModel.from_pretrained(model_name)

    segment = payload['translated_segment']

    # The predict method for embedding models expects a list of text instances
    embeddings = model.predict(instances=[segment])

    return {
        'translated_segment': segment,
        'embedding': embeddings.predictions[0],
        'model_id': model_name,
        'project_id': project_id,
        'location': location
    }
