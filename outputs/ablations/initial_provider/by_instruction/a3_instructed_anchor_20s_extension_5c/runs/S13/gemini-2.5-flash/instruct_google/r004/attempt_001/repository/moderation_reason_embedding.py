import os
from typing import List
import vertexai
from vertexai.language_models import TextEmbeddingModel

def moderation_reason_embedding(texts: List[str], project_id: str = None, location: str = "us-central1") -> List[List[float]]:
    project_id = project_id or os.environ.get("GOOGLE_PROJECT_ID")
    if not project_id:
        raise ValueError("Google Project ID not provided and not found in GOOGLE_PROJECT_ID environment variable.")

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")

    embeddings = []
    for text_content in texts:
        # The Vertex AI embedding model expects a list of instances. Each instance can be a dictionary.
        # The model's predict method takes a list of text inputs.
        response = model.get_embeddings([text_content])
        embeddings.append(response[0].values)

    return embeddings
