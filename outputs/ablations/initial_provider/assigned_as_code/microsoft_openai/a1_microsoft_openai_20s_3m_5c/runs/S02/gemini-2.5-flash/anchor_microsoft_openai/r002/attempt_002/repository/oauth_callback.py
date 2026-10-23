import msal
import os


def handle_oauth_callback(payload, config=None):
    config = config or {}
    app = msal.ConfidentialClientApplication(
        os.environ.get("AZURE_CLIENT_ID"),
        authority=f"https://login.microsoftonline.com/{os.environ.get('AZURE_TENANT_ID')}",
        client_credential=os.environ.get("AZURE_CLIENT_SECRET")
    )

    result = app.acquire_token_by_authorization_code(
        payload['code'],
        scopes=config.get('scopes', ['User.Read']),
        redirect_uri=payload['redirect_uri']
    )

    if "access_token" in result:
        return {
            "access_token": result["access_token"],
            "id_token": result.get("id_token"),
            "expires_in": result["expires_in"]
        }
    else:
        raise Exception(f"Failed to acquire token: {result.get('error_description', 'Unknown error')}")
