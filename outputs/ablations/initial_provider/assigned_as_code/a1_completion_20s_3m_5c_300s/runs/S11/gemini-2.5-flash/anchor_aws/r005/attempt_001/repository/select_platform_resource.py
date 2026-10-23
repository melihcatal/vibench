import boto3

def select_platform_resource(model_name, region="us-east-1"):
    client = boto3.client("bedrock", region_name=region)
    # This is a simplified example. In a real scenario, you would list
    # available models or deployments and filter based on model_name.
    # For now, we'll just return a placeholder based on the input.
    if model_name == "amazon.titan-text-express-v1":
        return {"model_id": "amazon.titan-text-express-v1"}
    elif model_name == "anthropic.claude-3-sonnet-20240229-v1:0":
        return {"model_id": "anthropic.claude-3-sonnet-20240229-v1:0"}
    else:
        return {"model_id": "us.amazon.nova-pro-v1:0"}

