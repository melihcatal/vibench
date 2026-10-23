from embeddings_client import create_client, invoke_batch_embeddings
from embeddings_models import normalize_texts


def embedding_job_summary(payload, config=None):
    client, cfg = create_client(config)
    texts = normalize_texts(payload["texts"])
    embeddings = invoke_batch_embeddings(client, cfg["model_id"], texts)
    return {"job_count": len(texts), "embedded_count": len(embeddings), "embeddings": embeddings}
