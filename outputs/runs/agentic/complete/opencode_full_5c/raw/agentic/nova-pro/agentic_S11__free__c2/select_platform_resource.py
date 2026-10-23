from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="your-api-key",
    api_version="2023-05-15",
    azure_endpoint="https://your-resource.openai.azure.com/",
)


def select_model():
    model_id = "your-model-id"
    return model_id
