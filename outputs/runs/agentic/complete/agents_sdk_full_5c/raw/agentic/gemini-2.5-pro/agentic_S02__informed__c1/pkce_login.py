from identity_client import get_msal_public_app, SCOPES

def start_pkce_flow(redirect_uri: str):
    """
    Starts a PKCE authorization flow for a public client.
    
    Returns a dictionary containing the authorization URI, state, and code verifier.
    The code_verifier must be stored securely (e.g., session) to be used later.
    """
    app = get_msal_public_app()
    
    flow = app.initiate_auth_code_flow(
        scopes=SCOPES,
        redirect_uri=redirect_uri,
    )
    
    return {
        "authorization_url": flow["auth_uri"],
        "state": flow["state"],
        "code_verifier": flow["code_verifier"],
    }

def complete_pkce_flow(authorization_code: str, code_verifier: str, redirect_uri: str):
    """
    Completes the PKCE flow by exchanging the authorization code for tokens.
    """
    app = get_msal_public_app()
    
    result = app.acquire_token_by_auth_code_flow(
        auth_code_flow={"code": authorization_code, "code_verifier": code_verifier},
        auth_response={"code": authorization_code},
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    if "error" in result:
        return {"error": result.get("error"), "error_description": result.get("error_description")}

    return result
