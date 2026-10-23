from embeddings_client import load_config, invoke_embeddings


def embedding_job_summary(job_texts):
    cfg = load_config()
    total = len(job_texts)
    response = invoke_embeddings(cfg.model_id, {"inputText": "job summary"}, cfg.region_name)
    return {"provider": "aws_bedrock", "model_id": cfg.model_id, "total_items": total, "response": response}
