import vertexai
from vertexai.language_models import TextEmbeddingModel
from storage_client import get_project_id

def asset_metadata_embedding(text_to_embed: str):
    vertexai.init(project=get_project_id(), location="us-central1")
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003")
    embeddings = model.get_embeddings([text_to_embed])
    
    return {"embedding": embeddings[0].values}
