
import os
import uuid
from identity_client import IdentityClient

def start_oauth_login() -> str:
    client = IdentityClient()
    
    # In a real application, 'state' would be stored in a secure, http-only, same-site cookie
    # or server-side session to prevent CSRF attacks.
    state = str(uuid.uuid4())
    
    # For simplicity, we are not implementing PKCE here, but it would be generated and stored as well.
    # code_verifier = str(uuid.uuid4())
    # code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).hexdigest()
    # code_challenge_base64 = base64.urlsafe_b64encode(code_challenge.encode('utf-8')).decode('utf-8').replace('=', '')

    authorization_url = client.get_authorization_url(state=state)
    print(f"Redirect to: {authorization_url}")
    return authorization_url

if __name__ == '__main__':
    # Example usage: Set environment variables for testing
    os.environ['AZURE_AD_CLIENT_ID'] = 'YOUR_AZURE_AD_CLIENT_ID'
    os.environ['AZURE_AD_REDIRECT_URI'] = 'http://localhost:5000/callback'
    start_oauth_login()
