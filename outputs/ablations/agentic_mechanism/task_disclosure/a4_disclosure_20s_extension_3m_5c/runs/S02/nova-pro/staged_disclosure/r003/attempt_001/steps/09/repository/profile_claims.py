import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up the service account credentials
SERVICE_ACCOUNT_FILE = 'path/to/service-account-file.json'
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the service
service = build('people', 'v1', credentials=credentials)


def fetch_profile_claims(person_id):
    """Fetches and normalizes federated user profile claims."""
    try:
        # Fetch the person
        results = service.people().get(resourceName=person_id, personFields='names,emailAddresses').execute()
        
        # Normalize the claims
        claims = {
            'name': results.get('names', [{}])[0].get('displayName', ''),
            'email': results.get('emailAddresses', [{}])[0].get('value', '')
        }
        return claims
    except Exception as e:
        print(f'An error occurred: {e}')
        return None


if __name__ == '__main__':
    # Example usage
    person_id = 'people/me'
    claims = fetch_profile_claims(person_id)
    print(claims)