import google.auth
from google.oauth2 import service_account

def fetch_profile_claims(credentials):
    service = google.auth.default()[0]
    profile = service.get('https://www.googleapis.com/oauth2/v1/userinfo')
    return profile