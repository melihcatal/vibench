import json
from model_client import get_bedrock_metadata_client

def select_bedrock_model(provider="Anthropic"):
    """
    Selects a foundation model from Amazon Bedrock based on provider.
    
    Returns:
        The model ID of the first found model from the specified provider.
    """
    bedrock_client = get_bedrock_metadata_client()
    
    try:
        response = bedrock_client.list_foundation_models(
            byProvider=provider
        )
        
        models = response.get("modelSummaries", [])
        if not models:
            raise ValueError(f"No models found for provider: {provider}")
        
        # Select the first model in the list
        selected_model = models[0]
        print(f"Selected model: {selected_model['modelId']}")
        return selected_model['modelId']

    except Exception as e:
        print(f"Error listing foundation models: {e}")
        return None

if __name__ == '__main__':
    # This part is for demonstration if run directly
    # and will not be executed in the main workflow.
    print("Attempting to select a Bedrock model...")
    model_id = select_bedrock_model()
    if model_id:
        print(f"Successfully selected model ID: {model_id}")
    else:
        print("Failed to select a model.")
