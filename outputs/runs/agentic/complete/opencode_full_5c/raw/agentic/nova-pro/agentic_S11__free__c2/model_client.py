from openai import AzureOpenAI


def get_client():
    api_key = "your-api-key"
    api_version = "2023-05-15"
    azure_endpoint = "https://your-resource.openai.azure.com/"
    return AzureOpenAI(
        api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint
    )
