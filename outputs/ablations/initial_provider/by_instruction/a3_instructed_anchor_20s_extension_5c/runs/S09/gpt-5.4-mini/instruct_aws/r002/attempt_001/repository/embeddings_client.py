import os
from dataclasses import dataclass

import boto3


@dataclass(frozen=True)
class EmbeddingsConfig:
    region_name: str
    model_id: str


def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        region_name=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        model_id=os.environ.get("BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
    )


def bedrock_runtime_client():
    config = load_config()
    return boto3.client("bedrock-runtime", region_name=config.region_name), config
