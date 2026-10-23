import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)


def collect_metadata(prompt):
    response = client.completions.create(
        model="text-davinci-003", prompt=prompt, max_tokens=150
    )
    return {
        "output": response.choices[0].text.strip(),
        "metadata": response.model_dump(),
    }
