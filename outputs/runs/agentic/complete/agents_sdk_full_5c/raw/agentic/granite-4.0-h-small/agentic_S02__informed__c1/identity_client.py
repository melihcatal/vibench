import os
from typing import Dict, Any
from identity_models import AuthCodeResponse, TokenSet, ProfileClaims

# Microsoft Entra ID (Azure AD) section – placeholder variables
class AzureIdentityClient:
    '''Minimal wrapper around MSAL for Azure AD authentication.'''
    def __init__(self):
        self.client_id = os.getenv('AZURE_CLIENT_ID')
        self.client_secret = os.getenv('AZURE_CLIENT_SECRET')
        self.tenant_id = os.getenv('AZURE_TENANT_ID')
        self.authority = f'https://login.microsoftonline.com/{self.tenant_id}'
        self.app = self._create_msal_app()

    def _create_msal_app(self):
        import msal
        return msal.ConfidentialClientApplication(
            client_id=self.client_id,
            authority=self.authority,
            client_credential=self.client_secret,
        )

    def exchange_code_for_tokens(self, auth_code: str):
        '''Exchange an authorization code for MSAL token response.'''
        token_resp = self.app.acquire_token_by_authorization_code(
            auth_code,
            scopes=['openid', 'profile', 'email'],
            redirect_uri='http://localhost:5000/oauth_callback',
        )
        # Convert raw dict to our local model
        return AuthCodeResponse(**token_resp)

    def fetch_cognito_profile(self, id_token: str) -> Dict[str, Any]:
        '''Stub for profile extraction; replace with real JWT parsing if needed.'''
        # Simple JWT payload extraction (no verification for demo purposes)
        payload = id_token.split('.')[1]
        decoded = self._base64url_decode(payload)
        return json.loads(decoded)

# Placeholder for additional providers (Cognito, etc.)
class FederatedIdentityClient:
    '''Unified client that can delegate to provider-specific implementations.'''
    def __init__(self):
        # Example: we could keep a dict of provider clients keyed by provider name
        self.azure = AzureIdentityClient()

    def exchange_code_for_tokens(self, auth_code: str) -> TokenSet:
        '''Public API used by oauth_callback and profile_claims.'''
        token_resp = self.azure.exchange_code_for_tokens(auth_code)
        return TokenSet(**token_resp)

    def get_profile(self, access_token: str) -> ProfileClaims:
        '''Obtain normalized profile claims from access token.'''
        # Placeholder: in real code call cognito, aws sts, or other provider-specific logic
        # Here we just return a dummy ProfileClaims for illustration.
        return ProfileClaims(
            user_id='demo_user_123',
            email='user@example.com',
            email_verified=True,
            given_name='Jane',
            family_name='Doe',
            picture_url='https://example.com/avatar.jpg',
        )

# Utility to decode base64url (used in JWT handling)
import base64, json

@staticmethod
def _base64url_decode(input_: str) -> str:
    rem = len(input_) % 4
    if rem > 0:
        input_ += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_.encode())
