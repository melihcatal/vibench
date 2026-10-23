from google.cloud import aiplatform
import os

def get_text_embedding(text: str) -> list[float]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
    aiplatform.init(project=project_id, location=location)
    
    model_id = "text-embedding-004"
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_id)
    
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
