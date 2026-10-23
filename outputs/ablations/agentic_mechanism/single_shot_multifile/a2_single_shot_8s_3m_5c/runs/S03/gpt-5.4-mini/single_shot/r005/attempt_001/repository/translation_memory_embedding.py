from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel


def translation_memory_embedding(texts, model_name='text-embedding-004'):
    aiplatform.init()
    model = TextEmbeddingModel.from_pretrained(model_name)
    embeddings = model.get_embeddings(texts)
    return [list(embedding.values) for embedding in embeddings]
