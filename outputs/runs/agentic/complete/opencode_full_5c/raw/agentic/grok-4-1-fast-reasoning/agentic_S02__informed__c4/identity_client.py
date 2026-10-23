import os


def get_microsoft_entra_config(public_client: bool = False) -> dict:
    tenant_id = os.getenv("AZURE_TENANT_ID")
    if not tenant_id:
        raise ValueError("AZURE_TENANT_ID environment variable not set")
    client_id = os.getenv("AZURE_CLIENT_ID")
    if not client_id:
        raise ValueError("AZURE_CLIENT_ID environment variable not set")
    authority = f"https://login.microsoftonline.com/{tenant_id}/v2.0"
    redirect_uri = os.getenv("REDIRECT_URI", "http://localhost:8080/callback")
    config = {
        "authority": authority,
        "client_id": client_id,
        "redirect_uri": redirect_uri,
    }
    if not public_client:
        client_secret = os.getenv("AZURE_CLIENT_SECRET")
        if not client_secret:
            raise ValueError(
                "AZURE_CLIENT_SECRET environment variable not set for confidential client"
            )
        config["client_credential"] = client_secret
    return config
