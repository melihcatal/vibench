from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_text_for_memory(text_segment: str, config: dict = None) -> dict:
    config = config or {}
    project_id = config['project_id']
    location = config.get('location', 'us-central1') # Vertex AI typically requires a region

    vertexai.init(project=project_id, location=location)

    # Using a pre-trained text embedding model from Vertex AI
    # Model name: text-embedding-004 or text-embedding-gecko@001
    model = TextEmbeddingModel.from_pretrained("text-embedding-gecko@001")

    embeddings = model.get_embeddings([text_segment])

    # The get_embeddings method returns a list of Embedding objects. We need the values from the first one.
    embedding_values = embeddings[0].values if embeddings else []

    return {
        "text_segment": text_segment,
        "embedding": embedding_values
    }
