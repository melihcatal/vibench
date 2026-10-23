import os
import google.auth
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up the credentials
credentials, project = google.auth.default()

# Build the service
service = build('oauth2', 'v2', credentials=credentials)

def fetch_profile_claims(user_id):
    # Fetch the user info
    user_info = service.userinfo().get(userId=user_id).execute()
    
    # Normalize the claims
    normalized_claims = {
        'name': user_info.get('name', ''),
        'email': user_info.get('email', ''),
        'picture': user_info.get('picture', '')
    }
    return normalized_claims