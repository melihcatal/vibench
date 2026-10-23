from msal import ConfidentialClientApplication


def refresh_session(refresh_token):
    client = ConfidentialClientApplication(
        client_id="your_client_id",
        client_credential="your_client_secret",
        authority="https://login.microsoftonline.com/your_tenant_id",
    )
    result = client.acquire_token_by_refresh_token(refresh_token)
    return result
