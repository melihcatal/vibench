import msal

def create_confidential_client(client_id, tenant_id, client_secret):
    return msal.ConfidentialClientApplication(
        client_id, authority=f"https://login.microsoftonline.com/{tenant_id}",
        client_credential=client_secret)