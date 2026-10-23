import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def fetch_profile_claims(user_id):
    # Load the service account key
    service_account_info = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY'))
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=['https://www.googleapis.com/auth/contacts.readonly']
    )
    
    # Build the service
    service = build('people', 'v1', credentials=credentials)
    
    # Fetch the profile
    profile = service.people().get(resourceName='people/' + user_id, personFields='names,emailAddresses').execute()
    
    # Normalize the profile claims
    normalized_claims = {
        'name': profile.get('names', [{}])[0].get('displayName', ''),
        'email': profile.get('emailAddresses', [{}])[0].get('value', '')
    }
    
    return normalized_claims