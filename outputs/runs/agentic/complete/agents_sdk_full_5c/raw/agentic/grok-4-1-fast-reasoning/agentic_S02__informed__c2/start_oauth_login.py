import os
import msal
from identity_client import get_config, generate_state

config = get_config()

app = msal.PublicClientApplication(
    config["client_id"],
    authority=config["authority"]
)

def start_oauth_login():
    state = generate_state()
    auth_url = app.get_authorization_request_url(
        config["scopes"],
        redirect_uri=config["redirect_uri"],
        state=state
    )
    return auth_url, state

# Provider-specific: msal SDK, AZURE_TENANT_ID env, Microsoft Entra authority