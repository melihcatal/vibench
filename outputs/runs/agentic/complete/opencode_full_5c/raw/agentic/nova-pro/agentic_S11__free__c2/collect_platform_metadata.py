from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="your-api-key",
    api_version="2023-05-15",
    azure_endpoint="https://your-resource.openai.azure.com/",
)


def collect_metadata(model_id, input_data):
    response = client.completions.create(model=model_id, prompt=input_data)
    metadata = {
        "usage": response.usage,
        "model_id": model_id,
        "output": response.choices[0].text.strip(),
    }
    return metadata
