import os
import google.auth
from googleapiclient.discovery import build

def fetch_and_normalize_profile_claims(access_token):
    credentials, project = google.auth.default()
    service = build('people', 'v1', credentials=credentials)
    
    # Fetch user profile
    profile = service.people().get(resourceName='people/me', personFields='names,emailAddresses').execute()
    
    # Normalize profile claims
    normalized_claims = {
        'name': profile.get('names', [{}])[0].get('displayName', ''),
        'email': profile.get('emailAddresses', [{}])[0].get('value', '')
    }
    return normalized_claims