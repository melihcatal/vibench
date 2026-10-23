from observability_client import ObservabilityClient

def embed_log_message(log_message_text, config=None):
    config = config or {}
    client = ObservabilityClient(project_id=config["project_id"])
    embedding_model = client.get_embedding_model()

    embeddings = embedding_model.get_embeddings([log_message_text])

    return {
        "log_message": log_message_text,
        "embedding": embeddings[0].values,
    }
