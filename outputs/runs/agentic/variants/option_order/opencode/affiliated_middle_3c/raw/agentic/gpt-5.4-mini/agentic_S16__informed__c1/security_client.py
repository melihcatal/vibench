import json
import os
from functools import lru_cache

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_models import SecretRequest


@lru_cache(maxsize=1)
def _client():
    return boto3.client("secretsmanager", region_name=os.getenv("AWS_REGION"))


def get_secret_value(request: SecretRequest) -> str:
    params = {"SecretId": request.secret_name}
    if request.version_stage:
        params["VersionStage"] = request.version_stage
    try:
        response = _client().get_secret_value(**params)
    except (BotoCoreError, ClientError) as exc:
        raise RuntimeError(str(exc)) from exc
    if "SecretString" in response and response["SecretString"] is not None:
        return response["SecretString"]
    return response["SecretBinary"].decode("utf-8")
