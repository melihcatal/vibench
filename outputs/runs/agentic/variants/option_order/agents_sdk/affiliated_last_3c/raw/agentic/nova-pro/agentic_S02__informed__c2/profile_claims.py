import os
from msal import PublicClientApplication

client_id = os.getenv('AZURE_CLIENT_ID')
tenant_id = os.getenv('AZURE_TENANT_ID')

app = PublicClientApplication(client_id, authority=f'https://login.microsoftonline.com/{tenant_id}')

scopes = ['user.read']
result = app.acquire_token_silent(scopes, account=None)

if 'access_token' in result:
    # Use the access token to fetch user profile claims
    pass
else:
    print('User is not logged in.')