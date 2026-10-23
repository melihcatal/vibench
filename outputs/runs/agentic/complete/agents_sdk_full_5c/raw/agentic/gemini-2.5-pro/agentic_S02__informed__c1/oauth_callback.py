from identity_client import get_msal_app, REDIRECT_PATH, SCOPES

def handle_callback(authorization_response: dict, state: str, redirect_uri: str):
    """
    Handles the OAuth callback, exchanging the authorization code for tokens.
    
    :param authorization_response: The full query string parameters from the callback.
    :param state: The 'state' value stored in the user's session.
    :param redirect_uri: The redirect URI used in the initial authorization request.
    :return: The token acquisition result dictionary or an error dictionary.
    """
    app = get_msal_app()

    result = app.acquire_token_by_auth_code_flow(
        auth_code_flow={"state": state, **authorization_response},
        auth_response=authorization_response,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )

    if "error" in result:
        return {"error": result.get("error"), "error_description": result.get("error_description")}

    return result
