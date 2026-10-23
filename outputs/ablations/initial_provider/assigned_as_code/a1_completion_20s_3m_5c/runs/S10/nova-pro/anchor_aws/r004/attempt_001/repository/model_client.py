import boto3


def get_bedrock_client(region=None):
    return boto3.client("bedrock-runtime", region_name=region)


def get_model_id(model_family):
    model_map = {
        "nova-pro": "amazon.nova-pro-v1:0",
    }
    return model_map.get(model_family)