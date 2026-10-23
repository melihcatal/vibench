from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="your-api-key",
    api_version="2023-05-15",
    azure_endpoint="https://your-resource.openai.azure.com/",
)


def stream_generation(model_id, input_data):
    response = client.completions.create(model=model_id, prompt=input_data, stream=True)
    for chunk in response:
        yield chunk.choices[0].text
