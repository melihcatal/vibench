import boto3

def select_platform_resource(model_name: str = "us.amazon.nova-pro-v1:0", region: str = "us-east-1"):
    # In a real scenario, this function might involve calling AWS APIs
    # like list_foundation_models or describe_custom_model to verify
    # model availability or fetch details based on `model_name`.
    # For this exercise, we'll assume the model_name directly maps to a Bedrock modelId.
    
    # Example: A more complex implementation might use boto3 to dynamically discover models.
    # client = boto3.client("bedrock", region_name=region)
    # response = client.list_foundation_models()
    # available_models = [m for m in response["modelSummaries"] if m["modelId"] == model_name]
    # if not available_models:
    #     raise ValueError(f"Model '{model_name}' not found in region '{region}'")
    
    return {"model_id": model_name, "region": region}
