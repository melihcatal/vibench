import vertexai
from vertexai.preview.language_models import TextEmbeddingModel
import os

def transcript_embedding(text_segment: str, project_id: str, location: str = 'us-central1'):
    # Before running, ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # pointing to your service account key file, and gcloud is configured.
    # Example: os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/path/to/your/keyfile.json"

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    
    embeddings = model.get_embeddings([text_segment])
    return [embedding.values for embedding in embeddings]
