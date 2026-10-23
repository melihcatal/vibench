import msal
import secrets

def pkce_login(config):
    app = msal.PublicClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}")
    code_verifier = secrets.token_bytes(32)
    code_challenge = msal.compute_code_challenge(code_verifier)
    authorization_request_url = app.get_authorization_request_url(
        config.get('scopes', ['User.Read']),
        redirect_uri=config['redirect_uri'],
        code_challenge=code_challenge,
        code_challenge_method='S256')
    return {'authorization_url': authorization_request_url, 'code_verifier': code_verifier.decode()}