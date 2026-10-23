import os
import vertexai
from vertexai.language_models import TextEmbeddingModel

def caption_embedding(caption_chunk: str, project_id: str, location: str = "us-central1"):
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = model.get_embeddings([caption_chunk])
    
    # The embeddings object contains a list of Embedding objects. 
    # Each Embedding object has a 'values' attribute which is a list of floats.
    # For a single caption_chunk, there will be one Embedding object.
    return embeddings[0].values
