import os

def select_platform_resource(preferred_model: str | None = None) -> str:
    """
    Resolves a provider-specific model, deployment, or inference resource before invocation.
    For OpenAI, this function selects a model name.
    """
    # Example: Prioritize preferred_model, then environment variable, then a default
    if preferred_model:
        return preferred_model
    
    env_model = os.environ.get("OPENAI_MODEL_NAME")
    if env_model:
        return env_model
    
    return "gpt-4"  # Default OpenAI model
