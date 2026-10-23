from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up the OAuth2 client
credentials = service_account.Credentials.from_service_account_file(
    'path/to/service-account.json',
    scopes=['https://www.googleapis.com/auth/userinfo.profile']
)

service = build('oauth2', 'v2', credentials=credentials)


def fetch_profile_claims(access_token):
    """Fetches user profile claims using the Google OAuth2 API."""
    try:
        profile = service.userinfo().get().execute()
        return profile
    except Exception as e:
        print(f'Error fetching profile claims: {e}')
        return None


def normalize_profile_claims(profile):
    """Normalizes user profile claims."""
    normalized_claims = {
        'name': profile.get('name', ''),
        'email': profile.get('email', ''),
        'picture': profile.get('picture', ''),
    }
    return normalized_claims