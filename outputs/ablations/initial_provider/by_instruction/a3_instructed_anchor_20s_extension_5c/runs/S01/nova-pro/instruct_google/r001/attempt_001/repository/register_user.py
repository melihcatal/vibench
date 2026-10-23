from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.cloud import identity

# Configuration
PROJECT_ID = 'your-project-id'
SERVICE_ACCOUNT_KEY_PATH = 'path/to/service-account-key.json'

# Initialize client
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_KEY_PATH,
    scopes=['https://www.googleapis.com/auth/cloud-identity.readonly']
)
client = identity.IdentityServiceClient(credentials=credentials)

# Function to register a new user
def register_user(email, password):
    user = identity.User()
    user.primary_email = email
    user.name = identity.UserName(given_name='User', family_name='Test')
    user.password = password
    parent = f'projects/{PROJECT_ID}'
    response = client.create_user(parent=parent, user=user)
    return response