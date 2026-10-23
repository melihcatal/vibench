import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3


@dataclass(frozen=True)
class EmbeddingsConfig:
    region_name: str
    model_id: str


def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        model_id=os.getenv("AWS_BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
    )


@lru_cache(maxsize=1)
def get_bedrock_runtime_client(region_name: Optional[str] = None):
    cfg = load_config()
    return boto3.client("bedrock-runtime", region_name=region_name or cfg.region_name)


def invoke_embeddings(model_id: str, body: Dict[str, Any], region_name: Optional[str] = None) -> Dict[str, Any]:
    client = get_bedrock_runtime_client(region_name)
    response = client.invoke_model(
        modelId=model_id,
        body=__import__("json").dumps(body).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    raw = response["body"].read()
    return __import__("json").loads(raw)
