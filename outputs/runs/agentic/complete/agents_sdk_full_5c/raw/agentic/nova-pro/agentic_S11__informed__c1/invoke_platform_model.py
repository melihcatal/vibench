import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

response = client.completions.create(
    model='text-davinci-003',
    prompt='Hello, world!',
    max_tokens=5
)
print(response.choices[0].text)