from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel

def embed_script(text: str, project_id: str, location: str = "us-central1") -> list[float]:
    model = TextEmbeddingModel.from_pretrained("textembedding-gecko@001") # Using a specific model identifier
    input_text = TextEmbeddingInput(text, task_type="SEMANTIC_SIMILARITY", title="script embedding")
    embeddings = model.get_embeddings([input_text])
    return embeddings[0].values
