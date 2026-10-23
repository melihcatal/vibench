import os
from authlib.integrations.flask_client import OAuth

# Configuration values for Auth0
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.environ.get("AUTH0_CLIENT_SECRET")
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

def configure_oauth_client(app):
    """
    Configures and registers the Auth0 OAuth client for a Flask application.
    """
    oauth = OAuth(app)
    oauth.register(
        "auth0",
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration"
    )
    return oauth

# Helper function to get user claims from a session token (example, not for production use without validation)
def get_user_claims(session_token):
    """
    Mocks extraction and normalization of user claims from a session token.
    In a real application, this would involve decoding and validating a JWT.
    """
    if session_token and "id_token" in session_token:
        # In a proper implementation, this would involve JWT decoding and validation:
        # from jose import jwt
        # decoded_token = jwt.decode(session_token["id_token"], ...)
        
        # Mocking claims extraction for this example:
        claims = {
            "sub": "user_id_mock_123",
            "name": "Mock User",
            "email": "mock.user@example.com",
            "picture": "https://example.com/mock_pic.jpg",
            "locale": "en-US"
        }
        
        normalized_claims = {
            "federated_id": claims.get("sub"),
            "display_name": claims.get("name"),
            "email_address": claims.get("email"),
            "profile_picture_url": claims.get("picture"),
            "preferred_language": claims.get("locale")
        }
        return normalized_claims
    return None
