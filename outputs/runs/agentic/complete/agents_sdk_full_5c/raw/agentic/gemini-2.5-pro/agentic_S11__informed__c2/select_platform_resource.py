from model_client import get_bedrock_client

def select_claude_sonnet_model():
    """
    Resolves a specific model, Anthropic Claude 3 Sonnet, from Amazon Bedrock.
    """
    bedrock_client = get_bedrock_client()
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    try:
        response = bedrock_client.get_foundation_model(modelIdentifier=model_id)
        return response.get("modelDetails")
    except bedrock_client.exceptions.ResourceNotFoundException:
        return None
