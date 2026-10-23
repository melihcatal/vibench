import os
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from typing import List

def embed_translated_segments(segments: List[str], project_id: str = None, location: str = None) -> List[List[float]]:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = location or os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project ID not provided or found in GOOGLE_CLOUD_PROJECT environment variable.")

    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@003") # Using textembedding-gecko@003 for embeddings

    embeddings = []
    for segment in segments:
        input_text = TextEmbeddingInput(text=segment, task_type="SEMANTIC_SIMILARITY")
        embedding = model.get_embeddings([input_text])[0].values
        embeddings.append(embedding)

    return embeddings
