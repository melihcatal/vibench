from google.cloud import aiplatform


def embed_script(
    text: str,
    project: str,
    location: str = "us-central1",
    model_name: str = "textembedding-gecko@003",
) -> list:
    aiplatform.init(project=project, location=location)
    model = aiplatform.TextEmbeddingModel.from_pretrained(model_name)
    embeddings = model.get_embeddings([text])
    return embeddings[0].values
