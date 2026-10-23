import boto3


def get_observability_client(region):
    return boto3.client("logs", region_name=region)


def get_config(region, log_group, log_stream):
    return {
        "region": region,
        "log_group": log_group,
        "log_stream": log_stream,
    }