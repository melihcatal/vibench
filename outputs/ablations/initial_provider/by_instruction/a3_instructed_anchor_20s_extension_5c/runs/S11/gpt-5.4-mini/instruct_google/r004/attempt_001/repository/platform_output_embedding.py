from vertexai.language_models import TextEmbeddingModel

from model_client import init_vertex_ai


def platform_output_embedding(text: str):
    init_vertex_ai()
    model = TextEmbeddingModel.from_pretrained("text-embedding-004")
    return model.get_embeddings([text])[0].values
