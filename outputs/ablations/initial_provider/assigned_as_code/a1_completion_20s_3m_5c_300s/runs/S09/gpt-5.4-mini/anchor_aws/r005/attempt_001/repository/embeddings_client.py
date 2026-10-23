import os
from dataclasses import dataclass

import boto3


@dataclass
class EmbeddingsConfig:
    region: str = os.getenv("AWS_REGION", "us-east-1")
    model_id: str = os.getenv("BEDROCK_EMBEDDINGS_MODEL_ID", "amazon.titan-embed-text-v2:0")


def load_config(config=None):
    base = EmbeddingsConfig()
    config = config or {}
    return {
        "region": config.get("region", base.region),
        "model_id": config.get("model_id", base.model_id),
    }


def bedrock_client(config=None):
    config = load_config(config)
    return boto3.client("bedrock-runtime", region_name=config["region"])


def model_id(config=None):
    return load_config(config)["model_id"]
