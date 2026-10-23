from typing import Iterable, List

from google.cloud import aiplatform
from vertexai.preview.language_models import TextEmbeddingModel


class CaptionEmbedder:
    def __init__(self, project_id: str, location: str = 'us-central1', model_name: str = 'text-embedding-004') -> None:
        self.project_id = project_id
        self.location = location
        self.model = TextEmbeddingModel.from_pretrained(model_name)

    def embed_chunks(self, chunks: Iterable[str]) -> List[List[float]]:
        embeddings = self.model.get_embeddings(list(chunks))
        return [list(embedding.values) for embedding in embeddings]
