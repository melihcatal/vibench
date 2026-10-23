import os
from functools import lru_cache

import boto3


def aws_region() -> str:
    return os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"


def bedrock_model_id() -> str:
    return os.getenv("BEDROCK_EMBEDDING_MODEL_ID") or "amazon.titan-embed-text-v2:0"


@lru_cache(maxsize=1)
def bedrock_runtime_client():
    return boto3.client("bedrock-runtime", region_name=aws_region())


def embedding_dimensions() -> int | None:
    value = os.getenv("BEDROCK_EMBEDDING_DIMENSIONS")
    return int(value) if value else None


def normalize_text(text: str) -> str:
    return " ".join(text.split())
