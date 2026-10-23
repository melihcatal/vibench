import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import boto3


@dataclass
class EmbeddingsConfig:
    aws_region: str
    aws_profile: Optional[str]
    model_id: str


def load_config() -> EmbeddingsConfig:
    return EmbeddingsConfig(
        aws_region=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        aws_profile=os.environ.get("AWS_PROFILE"),
        model_id=os.environ.get("AWS_BEDROCK_EMBEDDING_MODEL_ID", "amazon.titan-embed-text-v2:0"),
    )


def client():
    cfg = load_config()
    session = boto3.Session(profile_name=cfg.aws_profile, region_name=cfg.aws_region) if cfg.aws_profile else boto3.Session(region_name=cfg.aws_region)
    return session.client("bedrock-runtime")


def invoke_embeddings(payload: Dict[str, Any], model_id: Optional[str] = None) -> Dict[str, Any]:
    cfg = load_config()
    body = payload.copy()
    response = client().invoke_model(body=__import__("json").dumps(body), modelId=model_id or cfg.model_id, accept="application/json", contentType="application/json")
    return __import__("json").loads(response["body"].read())


def batch_texts(texts: List[str]) -> List[str]:
    return [str(text) for text in texts if str(text).strip()]
