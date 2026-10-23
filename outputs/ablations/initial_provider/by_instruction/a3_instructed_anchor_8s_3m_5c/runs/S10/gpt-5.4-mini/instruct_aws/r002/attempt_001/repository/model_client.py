import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

import boto3

DEFAULT_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


@dataclass(frozen=True)
class LLMConfig:
    region_name: str
    model_id: str


def load_config() -> LLMConfig:
    return LLMConfig(
        region_name=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")),
        model_id=os.getenv("BEDROCK_MODEL_ID", DEFAULT_MODEL_ID),
    )


@lru_cache(maxsize=1)
def bedrock_runtime_client(region_name: Optional[str] = None) -> Any:
    cfg = load_config()
    return boto3.client("bedrock-runtime", region_name=region_name or cfg.region_name)


def model_id_for_task(task_name: str) -> str:
    task_overrides: Dict[str, str] = {
        "summarize": os.getenv("BEDROCK_SUMMARY_MODEL_ID", DEFAULT_MODEL_ID),
        "extract_json": os.getenv("BEDROCK_JSON_MODEL_ID", DEFAULT_MODEL_ID),
        "answer": os.getenv("BEDROCK_QA_MODEL_ID", DEFAULT_MODEL_ID),
        "stream": os.getenv("BEDROCK_STREAM_MODEL_ID", DEFAULT_MODEL_ID),
        "safety": os.getenv("BEDROCK_SAFETY_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        "translate": os.getenv("BEDROCK_TRANSLATE_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
        "embed": os.getenv("BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-text-v1"),
        "spoken": os.getenv("BEDROCK_SPOKEN_MODEL_ID", DEFAULT_MODEL_ID),
    }
    return task_overrides.get(task_name, load_config().model_id)
