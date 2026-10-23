import os
from typing import Dict, Any

def get_oidc_config() -> Dict[str, Any]:
    return {
        "issuer": f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/v2.0",
        "authorization_endpoint": f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/authorize",
        "token_endpoint": f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/oauth2/v2.0/token",
        "jwks_uri": f"https://login.microsoftonline.com/{os.getenv('AZURE_TENANT_ID')}/discovery/v2.0/keys",
    }