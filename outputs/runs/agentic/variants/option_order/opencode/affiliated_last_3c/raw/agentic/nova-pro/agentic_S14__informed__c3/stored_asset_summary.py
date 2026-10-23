import os
from openai import AzureOpenAI


def stored_asset_summary(text):
    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version="2023-05-15",
        azure_endpoint=os.getenv("OPENAI_API_BASE"),
    )
    response = client.completions.create(
        model="text-davinci-003", prompt=text, max_tokens=150
    )
    print(f"Summary: {response.choices[0].text}")
    return response.choices[0].text
