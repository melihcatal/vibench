import boto3

def select_platform_resource(criteria=None, config=None):
    config = config or {}
    region = config.get("region", "us-east-1")
    client = boto3.client("bedrock", region_name=region)
    
    # Example: List available foundation models and filter based on criteria
    response = client.list_foundation_models()
    
    # A simplified example of filtering based on a hypothetical 'model_name_prefix'
    # In a real scenario, 'criteria' would be more complex (e.g., capability, cost)
    selected_model = None
    if criteria and "model_name_prefix" in criteria:
        for model in response["modelSummaries"]:
            if model["modelName"].startswith(criteria["model_name_prefix"]):
                selected_model = model
                break
    else:
        # Default to the first available model if no specific criteria
        if response["modelSummaries"]:
            selected_model = response["modelSummaries"][0]

    return {"selected_resource": selected_model}
