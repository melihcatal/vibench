import boto3

def get_bedrock_client(service_name: str = "bedrock-runtime", region_name: str = "us-east-1"):
    """Provides a configured boto3 client for AWS Bedrock."""
    return boto3.client(service_name, region_name=region_name)


def get_bedrock_model_id(model_alias: str = "nova"):
    """Resolves a model alias to a concrete Bedrock model ID."""
    # This is a simplified mapping. In a real application, this could be
    # loaded from configuration, a database, or dynamically discovered.
    model_map = {
        "nova": "us.amazon.nova-pro-v1:0",
        "claude-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
        "titan-text-express": "amazon.titan-text-express-v1"
    }
    return model_map.get(model_alias, model_alias)
