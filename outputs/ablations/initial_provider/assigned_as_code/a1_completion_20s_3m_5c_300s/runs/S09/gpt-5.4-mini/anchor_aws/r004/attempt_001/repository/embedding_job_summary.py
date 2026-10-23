from embeddings_client import get_bedrock_client, get_model_id, invoke_bedrock_json


def embedding_job_summary(payload, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    model_id = get_model_id(config)
    summary = invoke_bedrock_json(client, model_id, {"inputText": payload["job_text"]})
    return {"summary": summary.get("embedding", [])[:8]}
