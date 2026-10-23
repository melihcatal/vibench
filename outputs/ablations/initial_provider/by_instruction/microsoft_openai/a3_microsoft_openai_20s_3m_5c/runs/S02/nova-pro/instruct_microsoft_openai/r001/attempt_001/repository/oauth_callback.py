import msal

def oauth_callback(code, state):
    app = msal.PublicClientApplication(
        client_id="your-client-id",
        authority="https://login.microsoftonline.com/your-tenant-id",
        client_credential="your-client-secret"
    )
    result = app.acquire_token_by_auth_code_flow(state, {"code": code})
    if "access_token" in result:
        print("Token acquired")
    else:
        print(result.get("error"))
    return result