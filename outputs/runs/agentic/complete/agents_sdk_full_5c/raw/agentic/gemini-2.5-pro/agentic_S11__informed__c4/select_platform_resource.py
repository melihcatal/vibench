import os
from model_client import get_model_client, AZURE_OPENAI_CHAT_DEPLOYMENT_NAME

def resolve_deployment_model():
    """
    Resolves the Azure OpenAI deployment to be used.

    In a real-world scenario, this could involve looking up deployments
    based on certain criteria, checking their status, or selecting from a list.
    For this example, we resolve it from a pre-configured environment variable.
    The presence of the client and deployment name confirms the resource.
    """
    client = get_model_client()
    deployment_name = AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
    
    if not deployment_name:
        raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME environment variable not set.")

    # A simple way to "resolve" is to confirm we have a client and a deployment target.
    # A more complex resolution might involve listing deployments via the Azure API
    # and selecting one based on capabilities, e.g., a model that supports function calling.
    print(f"Resolved client for endpoint: {client.base_url}")
    print(f"Resolved deployment resource: {deployment_name}")
    
    return deployment_name

