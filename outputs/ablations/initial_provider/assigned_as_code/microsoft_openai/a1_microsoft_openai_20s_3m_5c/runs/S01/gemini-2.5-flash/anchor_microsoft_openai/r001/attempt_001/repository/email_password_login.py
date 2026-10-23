import msal
import os

def email_password_login(payload, config=None):
    config = config or {}
    # PublicClientApplication is used for ROPC flow
    app = msal.PublicClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}"
    )

    # The ROPC flow is generally not recommended due to security implications.
    # This is for demonstration purposes as requested by the prompt for direct email/password login.
    result = app.acquire_token_by_username_password(
        username=payload['email'],
        password=payload['password'],
        scopes=config.get('scopes', ['User.Read'])
    )

    if "access_token" not in result:
        raise RuntimeError(f"Microsoft Identity Platform authentication failed: {result.get('error_description', 'Unknown error')}")

    return {
        'access_token': result['access_token'],
        'refresh_token': result.get('refresh_token'),
        'id_token': result.get('id_token'),
        'expires_in': result.get('expires_in')
    }
