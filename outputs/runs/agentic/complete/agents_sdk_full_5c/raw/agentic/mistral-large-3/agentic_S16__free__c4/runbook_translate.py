import os
from google.cloud import translate_v2 as translate
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


def runbook_translate(target_language: str, vault_url: str = None) -> Dict[str, str]:
    """
    Translates secret-rotation runbook notes in Azure Key Vault using Google Cloud Translation.
    
    Args:
        target_language: Target language code (e.g., "es", "fr").
        vault_url: Azure Key Vault URL. Defaults to AZURE_KEY_VAULT_URL env var.
    
    Returns:
        A dictionary mapping secret names to translated runbook notes.
    """
    if vault_url is None:
        vault_url = os.getenv("AZURE_KEY_VAULT_URL")
    
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secrets = client.list_properties_of_secrets()
    
    translate_client = translate.Client()
    
    translations = {}
    for secret in secrets:
        tags = secret.tags or {}
        runbook_notes = tags.get("runbook_notes", "")
        if runbook_notes:
            result = translate_client.translate(
                runbook_notes,
                target_language=target_language
            )
            translations[secret.name] = result["translatedText"]
    
    return translations