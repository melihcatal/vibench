from model_client import create_client, get_model


def output_embedding(payload, config=None):
    config = config or {}
    with create_client(config) as client:
        response = client.models.embed_content(
            model=get_model(config, default="text-embedding-004"),
            contents=payload["text"],
        )
    embedding = getattr(response, "embedding", None)
    values = getattr(embedding, "values", None) if embedding is not None else None
    return {"embedding": list(values or [])}
