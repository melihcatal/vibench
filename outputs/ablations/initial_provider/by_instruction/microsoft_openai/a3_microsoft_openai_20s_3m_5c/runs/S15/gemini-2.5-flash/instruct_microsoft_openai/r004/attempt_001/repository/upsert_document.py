import os
from database_client import CosmosDBClient
from database_models import Document
from openai import AzureOpenAI

def upsert_document(document: Document):
    cosmos_client = CosmosDBClient()

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

    # Use OpenAI to process document content, e.g., generate a summary or tags
    document_text = str(document.content)
    response = openai_client.chat.completions.create(
        model=azure_openai_deployment_name, # or a specific model like "gpt-4o"
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes text."},
            {"role": "user", "content": f"Summarize the following document content: {document_text}"}
        ]
    )
    summary = response.choices[0].message.content

    # Add the generated summary to the document content before upserting
    document.content["summary"] = summary

    cosmos_client.container.upsert_item(body=document.to_dict())

