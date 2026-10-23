import os
from msal import PublicClientApplication

client_id = os.getenv('AZURE_CLIENT_ID')
tenant_id = os.getenv('AZURE_TENANT_ID')

app = PublicClientApplication(client_id, authority=f'https://login.microsoftonline.com/{tenant_id}')

scopes = ['user.read']
flow = app.initiate_auth_code_flow(scopes)

print(f'Please visit this URL to authorize: {flow["auth_uri"]}')
