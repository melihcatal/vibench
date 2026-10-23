import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_caption(text, project_id, location="us-central1"):
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko")

    embeddings = model.get_embeddings([text])
    # Assuming we want the first embedding vector for the single input text
    if embeddings and embeddings[0].values:
        return embeddings[0].values
    return None
