import secrets
import msal


def pkce_login(payload, config=None):
    config = config or {}
    app = msal.PublicClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}")
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = msal.create_code_challenge(code_verifier, method="S256")
    url = app.get_authorization_request_url(
        config.get('scopes', ['User.Read']),
        redirect_uri=payload['redirect_uri'],
        code_challenge=code_challenge,
        code_challenge_method="S256")
    return {'authorization_url': url, 'code_verifier': code_verifier}