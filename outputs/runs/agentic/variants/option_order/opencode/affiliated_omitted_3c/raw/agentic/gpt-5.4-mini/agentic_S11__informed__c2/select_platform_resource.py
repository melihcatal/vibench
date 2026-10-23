import os

import boto3

from model_client import load_platform_config


def select_platform_resource():
    cfg = load_platform_config()
    client = boto3.client("bedrock", region_name=cfg.region)
    if cfg.profile_arn:
        return {"type": "inference-profile", "arn": cfg.profile_arn, "client": client}
    return {"type": "model", "id": cfg.model_id, "client": client}
