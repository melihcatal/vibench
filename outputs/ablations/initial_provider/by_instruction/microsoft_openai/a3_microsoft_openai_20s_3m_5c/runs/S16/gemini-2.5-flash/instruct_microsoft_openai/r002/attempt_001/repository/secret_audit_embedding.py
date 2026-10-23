from openai import AzureOpenAI
import os

def embed_text(text: str) -> list[float]:
    azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    azure_openai_key = os.environ.get("AZURE_OPENAI_API_KEY")
    azure_openai_api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
    azure_openai_embedding_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME") # e.g., text-embedding-ada-002

    if not azure_openai_endpoint or not azure_openai_key or not azure_openai_embedding_deployment_name:
        raise ValueError("Azure OpenAI environment variables (ENDPOINT, KEY, EMBEDDING_DEPLOYMENT_NAME) must be set.")

    client = AzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version=azure_openai_api_version
    )

    response = client.embeddings.create(
        input=text,
        model=azure_openai_embedding_deployment_name
    )

    return response.data[0].embedding

def embed_secret_audit_note(audit_note: str) -> list[float]:
    return embed_text(audit_note)
