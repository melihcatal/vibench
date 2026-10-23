import os


def get_bedrock_config(config=None):
    cfg = dict(config or {})
    return {
        "region": cfg.get("region") or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1",
        "model_id": cfg.get("model_id") or os.getenv("BEDROCK_MODEL_ID") or "amazon.nova-pro-v1:0",
    }
