from openai import AzureOpenAI
import os

def embed_audit_note(audit_note: str, 
                     azure_openai_endpoint: str = None, 
                     azure_openai_key: str = None, 
                     azure_openai_deployment_name: str = None) -> list[float]:

    if not azure_openai_endpoint:
        azure_openai_endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
        if not azure_openai_endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable not set.")
    if not azure_openai_key:
        azure_openai_key = os.environ.get("AZURE_OPENAI_KEY")
        if not azure_openai_key:
            raise ValueError("AZURE_OPENAI_KEY environment variable not set.")
    if not azure_openai_deployment_name:
        azure_openai_deployment_name = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME")
        if not azure_openai_deployment_name:
            raise ValueError("AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME environment variable not set.")

    client = AzureOpenAI(
        azure_endpoint = azure_openai_endpoint,
        api_key = azure_openai_key,
        api_version = "2024-02-01"
    )

    response = client.embeddings.create(
        input=audit_note,
        model=azure_openai_deployment_name # Use the deployment name for Azure OpenAI
    )
    return response.data[0].embedding
