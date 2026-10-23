import msal


def get_identity_client():
    config = {
        'client_id': 'YOUR_CLIENT_ID',
        'tenant_id': 'YOUR_TENANT_ID',
        'client_secret': 'YOUR_CLIENT_SECRET'
    }
    app = msal.ConfidentialClientApplication(
        config['client_id'], authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        client_credential=config['client_secret'])
    return app