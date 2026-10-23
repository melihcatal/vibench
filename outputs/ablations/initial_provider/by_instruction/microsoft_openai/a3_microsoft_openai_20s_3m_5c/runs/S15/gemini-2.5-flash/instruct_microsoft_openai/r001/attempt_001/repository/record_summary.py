import os
from openai import AzureOpenAI

AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY = os.environ.get("AZURE_OPENAI_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")

def summarize_document_record(document_content: str) -> str:
    if not AZURE_OPENAI_ENDPOINT or not AZURE_OPENAI_KEY:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY must be set in environment variables")

    client = AzureOpenAI(
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
        api_version="2024-02-01",
    )

    response = client.chat.completions.create(
        model=AZURE_OPENAI_DEPLOYMENT_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user", "content": f"Please summarize the following document:

{document_content}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content
