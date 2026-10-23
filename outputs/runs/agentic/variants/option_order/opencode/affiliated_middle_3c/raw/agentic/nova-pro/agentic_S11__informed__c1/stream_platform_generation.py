import os
from openai import AzureOpenAI

os.environ["AZURE_OPENAI_API_KEY"] = "your-api-key"
os.environ["AZURE_OPENAI_ENDPOINT"] = "your-endpoint"
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2023-05-15",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
)


def stream_generation(prompt):
    response = client.completions.create(
        model="text-davinci-003", prompt=prompt, stream=True
    )
    for chunk in response:
        yield chunk
