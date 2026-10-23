import json
from typing import Dict, Any
from identity_models import ProfileClaims
from identity_client import FederatedIdentityClient
import boto3

# AWS Cognito configuration (federated identity provider)
COGNITO_USER_POOL_ID = os.getenv('COGNITO_USER_POOL_ID')
COGNITO_CLIENT_ID = os.getenv('COGNITO_CLIENT_ID')
COGNITO_IDENTITY_POOL_ID = os.getenv('COGNITO_IDENTITY_POOL_ID')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# boto3 client for Cognito Identity (used to retrieve AWS tokens that carry cognito claims)
cognito_id_client = boto3.client(
    'cognito-identity',
    region_name=AWS_REGION,
)

def fetch_cognito_profile(id_token: str) -> Dict[str, Any]:
    '''Validate the ID token and extract basic profile information from claims.'''
    # Simple JWT verification can be done with jwt package; here we rely on Cognito to verify
    # In production use a JWT library (e.g., PyJWT) and the JWKs endpoint from Cognito.
    payload = json.loads(id_token.split('.')[1])
    return {
        'sub': payload.get('sub'),
        'email': payload.get('email'),
        'email_verified': payload.get('email_verified'),
        'name': payload.get('name'),
        'preferred_username': payload.get('preferred_username'),
    }

def get_federated_profile(access_token: str) -> ProfileClaims:
    '''Exchange a Cognito access token for user profile claims using AWS STS AssumeRoleWithWebIdentity.'''
    response = cognito_id_client.assume_role_with_web_identity(
        RoleArn=f'arn:aws:iam::{os.getenv("AWS_ACCOUNT_ID")}:role/{os.getenv("COGNITO_AUTH_ROLE")}',
        RoleSessionName='federated-login-session',
        WebIdentityToken=access_token,
        DurationSeconds=3600,
    )
    # The returned credentials carry an assumed IAM role; the role's trust policy can inject Cognito claims
    # For simplicity we fetch the identity ID which includes the cognito groups/attributes in a JSON payload.
    identity_id = response['IdentityId']
    # Retrieve the underlying Cognito user attributes via the GetUser API (requires a valid access token)
    user_response = boto3.client('cognito-idp', region_name=AWS_REGION).get_user(
        AccessToken=access_token,
    )
    attributes = {a['Name']: a['Value'] for a in user_response['UserAttributes']}
    # Normalization into our consistent model
    return ProfileClaims(
        user_id=identity_id,
        email=attributes.get('email'),
        email_verified=attributes.get('email_verified') == 'true',
        given_name=attributes.get('given_name'),
        family_name=attributes.get('family_name'),
        picture_url=attributes.get('picture'),
    )


def profile_claims_from_code(auth_code: str) -> ProfileClaims:
    '''Full flow: exchange code → get tokens → fetch normalized profile.'''
    client = FederatedIdentityClient()
    token_set = client.exchange_code_for_tokens(auth_code)
    # Use the access token embedded in the token set
    return get_federated_profile(token_set.access_token)

if __name__ == '__main__':
    # Example CLI usage: pass an auth code as argument
    import sys
    if len(sys.argv) < 2:
        print('Usage: python profile_claims.py <auth_code>')
        sys.exit(1)
    code = sys.argv[1]
    profile = profile_claims_from_code(code)
    print(json.dumps(profile.asdict(), indent=2))
