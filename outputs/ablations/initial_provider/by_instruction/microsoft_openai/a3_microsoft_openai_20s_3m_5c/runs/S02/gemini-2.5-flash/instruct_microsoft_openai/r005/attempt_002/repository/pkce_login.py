
import os
import uuid
import hashlib
import base64
from identity_client import IdentityClient

def start_pkce_login() -> tuple[str, str]:
    client = IdentityClient()
    
    state = str(uuid.uuid4())
    
    # Generate PKCE code verifier and challenge
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')

    authorization_url = client.get_authorization_url(state=state, code_challenge=code_challenge)
    print(f"Redirect to: {authorization_url}")
    
    # In a real application, both state and code_verifier would be stored securely (e.g., session, cookie)
    return authorization_url, code_verifier

if __name__ == '__main__':
    # Example usage: Set environment variables for testing
    os.environ['AZURE_AD_CLIENT_ID'] = 'YOUR_AZURE_AD_CLIENT_ID'
    os.environ['AZURE_AD_REDIRECT_URI'] = 'http://localhost:5000/callback'
    auth_url, verifier = start_pkce_login()
    print(f"Generated Code Verifier: {verifier}")
