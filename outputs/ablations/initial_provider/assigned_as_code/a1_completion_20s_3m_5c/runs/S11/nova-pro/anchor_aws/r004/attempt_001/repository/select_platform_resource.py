import boto3


def select_platform_resource(config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region", "us-east-1"))
    response = client.list_foundation_models()
    model_id = response['modelSummaries'][0]['modelId']
    return model_id