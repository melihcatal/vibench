import os


def get_bedrock_model_id(model_name: str = "anthropic.claude-v2") -> str:
    """
    Resolves a model ID for Amazon Bedrock.
    This could be extended to look up models from a registry.
    """
    # In a real application, this might involve more complex logic,
    # like querying an API or a configuration file.
    # For this example, we use a default or an environment variable.
    return os.environ.get("BEDROCK_MODEL_ID", model_name)
