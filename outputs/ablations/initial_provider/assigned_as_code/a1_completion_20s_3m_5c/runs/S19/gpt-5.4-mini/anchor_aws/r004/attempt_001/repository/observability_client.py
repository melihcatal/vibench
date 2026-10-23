import os

import boto3


def load_observability_config(config=None):
    config = dict(config or {})
    if "region" not in config:
        config["region"] = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION")
    if "namespace" not in config:
        config["namespace"] = os.getenv("CLOUDWATCH_NAMESPACE", "ManagedMetricsMonitoring")
    return config


def cloudwatch_client(config=None):
    config = load_observability_config(config)
    return boto3.client("cloudwatch", region_name=config.get("region"))
