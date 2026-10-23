from model_client import get_bedrock_client

def find_anthropic_claude_model_id(provider: str = "anthropic") -> str:
    """
    Finds and returns the model ID for the latest available Anthropic Claude model.
    """
    bedrock_client = get_bedrock_client()
    response = bedrock_client.list_foundation_models()
    models = response.get("modelSummaries", [])

    claude_models = [
        m for m in models
        if provider in m.get("providerName", "").lower()
        and "claude" in m.get("modelName", "").lower()
        and not m.get("modelLifecycle", {}).get("status") == "LEGACY"
    ]

    if not claude_models:
        raise RuntimeError(f"No models found for provider {provider}")

    # Sort by model name to get the latest version, assuming higher version number is later
    claude_models.sort(key=lambda x: x["modelName"], reverse=True)
    
    return claude_models[0]["modelId"]
