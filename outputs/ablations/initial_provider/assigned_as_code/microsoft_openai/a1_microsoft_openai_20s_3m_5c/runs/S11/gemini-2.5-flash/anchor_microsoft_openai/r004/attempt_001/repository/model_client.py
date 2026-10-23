import os

class ManagedModelClientConfig:
    def __init__(self, provider: str, api_key_env_var: str, endpoint_env_var: str = None):
        self.provider = provider
        self.api_key = os.environ.get(api_key_env_var)
        self.endpoint = os.environ.get(endpoint_env_var) if endpoint_env_var else None

    def get_client_params(self):
        params = {"api_key": self.api_key}
        if self.endpoint:
            params["endpoint"] = self.endpoint
        return params

def get_provider_config(provider_name: str):
    # This is a simplified example. In a real application, this would load from a more robust config system.
    if provider_name == "openai":
        return ManagedModelClientConfig("openai", "OPENAI_API_KEY")
    elif provider_name == "azure_openai":
        return ManagedModelClientConfig("azure_openai", "AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT")
    elif provider_name == "google_vertex_ai":
        # Google Cloud auth typically uses ADC, so API key might not be direct
        return ManagedModelClientConfig("google_vertex_ai", "GOOGLE_APPLICATION_CREDENTIALS") # This is just a placeholder, typically not a direct API key
    elif provider_name == "aws_bedrock":
        # AWS Bedrock uses boto3 which handles auth via env vars, IAM roles, etc.
        return ManagedModelClientConfig("aws_bedrock", "AWS_ACCESS_KEY_ID") # Placeholder, actual usage is more complex
    elif provider_name == "cohere":
        return ManagedModelClientConfig("cohere", "COHERE_API_KEY")
    elif provider_name == "aws_polly":
        return ManagedModelClientConfig("aws_polly", "AWS_ACCESS_KEY_ID") # Placeholder, actual usage is more complex
    return None
