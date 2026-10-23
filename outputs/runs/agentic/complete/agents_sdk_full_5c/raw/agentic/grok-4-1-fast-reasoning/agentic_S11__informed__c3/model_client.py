import os

def get_platform_config() -> dict:
    """Get Azure OpenAI configuration."""
    return {
        "azure_endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "azure_api_key": os.getenv("AZURE_OPENAI_API_KEY"),
        "api_version": "2024-05-13",
        "deployment": "gpt-4o"
    }