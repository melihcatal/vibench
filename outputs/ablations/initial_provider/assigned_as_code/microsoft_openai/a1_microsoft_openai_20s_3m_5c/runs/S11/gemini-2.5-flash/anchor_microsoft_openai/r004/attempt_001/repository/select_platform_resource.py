import boto3

def select_platform_resource(model_name: str, region: str = "us-east-1"):
    bedrock = boto3.client(service_name="bedrock", region_name=region)
    # In a real scenario, you'd list models and find the ARN for model_name
    # For simplicity, we'll assume a direct mapping or a lookup is performed
    # This example directly constructs an ARN, which might not be how all models are referenced
    # For actual model listing, one would use:
    # response = bedrock.list_foundation_models()
    # Then filter by model_name
    
    # Example placeholder: This would be dynamic based on actual Bedrock model IDs
    if "titan" in model_name.lower():
        return f"arn:aws:bedrock:{region}::foundation-model/{model_name}"
    elif "claude" in model_name.lower():
        return f"arn:aws:bedrock:{region}::foundation-model/{model_name}"
    else:
        return f"arn:aws:bedrock:{region}::foundation-model/{model_name}"
