import msal

def oauth_callback(authority, client_id, redirect_uri, code):
    app = msal.PublicClientApplication(
        client_id, authority=authority
    )
    result = app.acquire_token_by_auth_code(code, redirect_uri=redirect_uri)
    return result