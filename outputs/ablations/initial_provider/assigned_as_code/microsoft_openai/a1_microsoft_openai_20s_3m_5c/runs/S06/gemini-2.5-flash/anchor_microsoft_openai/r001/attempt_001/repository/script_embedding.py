from google.cloud import aiplatform
import os

def embed_script(text, project_id=None, location='us-central1'):
    if not project_id:
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')

    aiplatform.init(project=project_id, location=location)

    model = aiplatform.TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings([text])

    return {"embedding": embeddings[0].values}