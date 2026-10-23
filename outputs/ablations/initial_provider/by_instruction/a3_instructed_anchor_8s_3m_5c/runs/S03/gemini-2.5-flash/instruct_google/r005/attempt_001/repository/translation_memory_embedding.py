import vertexai
from vertexai.language_models import TextEmbeddingModel

def embed_text_for_translation_memory(text: str, project_id: str, location: str = "us-central1") -> list[float]:
    vertexai.init(project=project_id, location=location)
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001")
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
