from embeddings_client import get_client, get_config, invoke_embedding


def embedding_job_summary(payload, config=None):
    config = get_config(config)
    client = get_client(config)
    raw = invoke_embedding(client, config["model_id"], {"inputText": payload["summary_text"]})
    return {"job_summary": raw}
