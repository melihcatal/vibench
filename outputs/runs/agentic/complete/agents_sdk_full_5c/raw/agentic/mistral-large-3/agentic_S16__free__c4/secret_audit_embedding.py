import os
import json
from openai import OpenAI
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def secret_audit_embedding(vault_url: str = None) -> Dict[str, list]:
    """
    Embeds secret audit notes from Azure Key Vault for semantic search using OpenAI.
    
    Args:
        vault_url: Azure Key Vault URL. Defaults to AZURE_KEY_VAULT_URL env var.
    
    Returns:
        A dictionary mapping secret names to their embedding vectors.
    """
    if vault_url is None:
        vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secrets = client.list_properties_of_secrets()
    
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    embeddings = {}
    for secret in secrets:
        tags = secret.tags or {}
        notes = tags.get("audit_notes", "")
        if notes:
            response = openai_client.embeddings.create(
                input=notes,
                model="text-embedding-ada-002"
            )
            embeddings[secret.name] = response.data[0].embedding
    
    return embeddings