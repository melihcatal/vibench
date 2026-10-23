from openai import AzureOpenAI
import os


def get_azure_openai_client(config):
    return AzureOpenAI(
        azure_endpoint=config.get("AZURE_OPENAI_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=config.get("AZURE_OPENAI_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=config.get("AZURE_OPENAI_API_VERSION", "2024-02-01"),
    )
