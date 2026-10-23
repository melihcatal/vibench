import os
from google.oauth2 import service_account

def get_identity_client():
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )
    return credentials

if __name__ == '__main__':
    client = get_identity_client()
    print(client)