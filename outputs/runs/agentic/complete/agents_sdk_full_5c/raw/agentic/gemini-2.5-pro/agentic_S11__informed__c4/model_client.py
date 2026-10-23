import os
from openai import AzureOpenAI

# It is recommended to use a different deployment for embeddings
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")

def get_model_client() -> AzureOpenAI:
    """
    Initializes and returns an AzureOpenAI client.
    
    Expects the following environment variables:
    - AZURE_OPENAI_ENDPOINT: The endpoint for your Azure OpenAI service.
    - AZURE_OPENAI_API_KEY: The API key for your Azure OpenAI service.
    - AZURE_OPENAI_API_VERSION: The API version to use.
    """
    return AzureOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    )
