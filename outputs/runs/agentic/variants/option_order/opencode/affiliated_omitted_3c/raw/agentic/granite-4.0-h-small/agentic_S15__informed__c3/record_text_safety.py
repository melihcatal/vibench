import json
from database_client import parse_response

# Provider: Azure AI Content Safety (SDK: azure-ai-contentsafety) – supports SDK and REST
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential

# Initialise client once (AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY env required)
endpoint = get_env_or_raise("AZURE_CONTENT_SAFETY_ENDPOINT")
key = get_env_or_raise("AZURE_CONTENT_SAFETY_KEY")
client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Choose the model (default provided by Azure)
model_id = "content-safety-text-moderation"  # concrete model for Azure

def check_text_safety(text: str) -> dict:
    """Analyze user‑generated text for unsafe content using Azure AI Content Safety.
    Args:
        text: The raw user‑provided string to evaluate.
    Returns:
        dict containing a boolean 'safe' flag and details from Azure.
    """
    response = client.analyze_text(text=text)
    result = response.to_dict()  # concrete shape depends on SDK version
    safe = result.get('safe', False)
    details = result.get('details', {})
    return {"safe": safe, "details": details}

# Helper for missing env variables
get_env_or_raise = lambda var: 
    os.getenv(var) or (lambda: (_ for _ in ()).throw(RuntimeError(f"Missing env {var}")))()()
