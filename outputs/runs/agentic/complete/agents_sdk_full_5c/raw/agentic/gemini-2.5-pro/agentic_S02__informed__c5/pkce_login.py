import msal
from typing import Dict, Any, Tuple
from identity_client import get_msal_client, get_msal_config

def start_entra_pkce_flow() -> Tuple[str, str, str]:
    """
    Initiates an authorization code flow with PKCE for Microsoft Entra ID.

    Returns:
        A tuple containing:
        - The authorization URL to redirect the user to.
        - The PKCE code verifier (must be stored securely in the user's session).
        - The flow state dictionary from msal (must be stored in the user's session).
    """
    msal_client = get_msal_client()
    config = get_msal_config()
    
    # This will generate a code_verifier and code_challenge internally
    flow = msal_client.initiate_auth_code_flow(
        scopes=config["scope"],
        redirect_uri=config["redirect_uri"]
    )

    auth_url = flow["auth_uri"]
    code_verifier = flow.get("code_verifier")
    
    return auth_url, code_verifier, flow

def complete_entra_pkce_flow(
    flow: Dict[str, Any],
    auth_response: Dict[str, Any],
    code_verifier: str
) -> Dict[str, Any]:
    """
    Completes the PKCE flow by exchanging the authorization code for a token.

    Args:
        flow: The flow state dictionary saved from the initiation step.
        auth_response: The dictionary of query parameters from the redirect URI.
        code_verifier: The PKCE code verifier saved from the initiation step.

    Returns:
        A dictionary containing the access token, id token, and user info.
    """
    msal_client = get_msal_client()
    config = get_msal_config()

    result = msal_client.acquire_token_by_auth_code_flow(
        auth_code_flow=flow,
        auth_response=auth_response,
        scopes=config["scope"],
        code_verifier=code_verifier
    )
    
    if "error" in result:
        raise Exception(f"MSAL Error: {result.get('error_description')}")
        
    return result
