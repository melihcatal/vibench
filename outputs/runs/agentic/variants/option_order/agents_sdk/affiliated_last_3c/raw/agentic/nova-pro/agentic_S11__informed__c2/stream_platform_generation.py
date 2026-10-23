import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

stream = client.chat.completions.create(
    model='gpt-35-turbo',
    messages=[{"role": "user", "content": "Hello, world!"}],
    stream=True
)
for chunk in stream:
    print(chunk)