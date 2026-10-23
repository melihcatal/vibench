import os
from openai import AzureOpenAI
from typing import Dict, Any

def summarize_record(record_content: Dict[str, Any]) -> str:
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
    azure_openai_deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME") # e.g., gpt-4o

    if not all([azure_openai_endpoint, azure_openai_key, azure_openai_deployment_name]):
        raise ValueError("Azure OpenAI environment variables not set. Please set AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY, AZURE_OPENAI_DEPLOYMENT_NAME.")

    openai_client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version="2024-02-15-preview" # Example API version
    )

    text_to_summarize = str(record_content)
    response = openai_client.chat.completions.create(
        model=azure_openai_deployment_name, 
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
            {"role": "user", "content": f"Please provide a brief summary of the following document record: {text_to_summarize}"}
        ]
    )
    summary = response.choices[0].message.content
    return summary
