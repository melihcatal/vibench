import os
from identity_client import get_msal_app, REDIRECT_PATH, SCOPES

def get_authorization_url(redirect_uri: str):
    """
    Generates an authorization URL for the Microsoft Identity Platform.
    """
    app = get_msal_app()
    
    auth_url_flow = app.initiate_auth_code_flow(
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    
    # The state is stored in the session for later validation
    # For this example, we just return it along with the URL
    return {
        "authorization_url": auth_url_flow["auth_uri"],
        "state": auth_url_flow["state"]
    }
