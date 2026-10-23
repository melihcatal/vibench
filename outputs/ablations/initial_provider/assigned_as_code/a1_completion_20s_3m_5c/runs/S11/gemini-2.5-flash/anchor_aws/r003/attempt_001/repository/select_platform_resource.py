import boto3

def select_platform_resource(model_query, config=None):
    config = config or {}
    # In a real scenario, this would involve a more sophisticated lookup
    # based on the model_query, e.g., querying Bedrock for available models
    # or a configuration service. For this exercise, we'll return a fixed model ID.
    if "amazon" in model_query.lower():
        model_id = "us.amazon.nova-pro-v1:0"
    else:
        model_id = "us.amazon.nova-pro-v1:0" # Defaulting for simplicity

    return {"model_id": model_id}
