import os
from dataclasses import dataclass

import boto3


@dataclass
class EmbeddingsClientConfig:
    region_name: str
    model_id: str


def load_config() -> EmbeddingsClientConfig:
    return EmbeddingsClientConfig(
        region_name=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        model_id=os.environ.get("AWS_BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
    )


def create_bedrock_runtime_client():
    cfg = load_config()
    return boto3.client("bedrock-runtime", region_name=cfg.region_name), cfg
