import vertexai
from vertexai.preview.language_models import TextEmbeddingModel
from speech_client import get_vertex_ai_embedding_model
from speech_models import EmbeddingOutput
from typing import List


def embed_script(text: str) -> EmbeddingOutput:
    model = get_vertex_ai_embedding_model()
    embeddings = model.get_embeddings([text])
    # Assuming we only pass one text, so we take the first embedding
    return EmbeddingOutput(embedding=embeddings[0].values)
