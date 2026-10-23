from model_client import client, default_model, normalize_text


def output_embedding(text: str, model: str | None = None):
    embedding_model = model or "text-embedding-004"
    response = client().models.embed_content(model=embedding_model, contents=normalize_text(text))
    return response.embedding.values
