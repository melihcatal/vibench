from embeddings_client import get_client, load_config


def embedding_job_summary(texts: list[str]) -> dict[str, object]:
    client = get_client()
    config = load_config()
    response = client.embed(
        texts=texts, model=config.model, input_type="search_document"
    )
    return {
        "model": config.model,
        "count": len(response.embeddings),
        "dimensions": len(response.embeddings[0]) if response.embeddings else 0,
    }
