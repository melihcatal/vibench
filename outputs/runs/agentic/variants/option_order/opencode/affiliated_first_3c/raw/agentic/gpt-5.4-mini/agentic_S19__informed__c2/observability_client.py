import os
from dataclasses import dataclass

import boto3


@dataclass
class ObservabilityConfig:
    region_name: str


def load_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        region_name=os.getenv(
            "AWS_REGION", os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        )
    )


def cloudwatch_client():
    cfg = load_config()
    return boto3.client("cloudwatch", region_name=cfg.region_name)


def normalize_dimensions(dimensions):
    if not dimensions:
        return []
    normalized = []
    for item in dimensions:
        if isinstance(item, dict) and "Name" in item and "Value" in item:
            normalized.append({"Name": str(item["Name"]), "Value": str(item["Value"])})
        elif isinstance(item, tuple) and len(item) == 2:
            normalized.append({"Name": str(item[0]), "Value": str(item[1])})
    return normalized
