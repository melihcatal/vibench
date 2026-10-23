import os
from typing import Any, Dict, Optional

import boto3


AWS_REGION_ENV = "AWS_REGION"
AWS_BEDROCK_MODEL_ENV = "BEDROCK_MODEL_ID"


def load_region() -> str:
    return os.getenv(AWS_REGION_ENV, "us-east-1")


def load_model_id(default: str) -> str:
    return os.getenv(AWS_BEDROCK_MODEL_ENV, default)


def bedrock_runtime_client(region: Optional[str] = None):
    return boto3.client("bedrock-runtime", region_name=region or load_region())


def invoke_json_model(client: Any, model_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=str(payload).replace("'", '"').encode("utf-8"),
    )
    body = response["body"].read()
    return {"body": body.decode("utf-8"), "response": response}
