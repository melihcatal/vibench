import os
from msal import PublicClientApplication

client_id = os.getenv('AZURE_CLIENT_ID')
tenant_id = os.getenv('AZURE_TENANT_ID')

app = PublicClientApplication(client_id, authority=f'https://login.microsoftonline.com/{tenant_id}')

token_response = app.acquire_token_by_auth_code_flow(flow, auth_code)

print(token_response)