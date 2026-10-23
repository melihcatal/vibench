import os

class IdentityClientConfig:
    """
    Provides configuration for various identity providers.
    """
    @staticmethod
    def get_cognito_config() -> dict:
        return {
            "CLIENT_ID": os.environ.get("COGNITO_CLIENT_ID"),
            "REDIRECT_URI": os.environ.get("COGNITO_REDIRECT_URI"),
            "DOMAIN": os.environ.get("COGNITO_DOMAIN"),
        }

    @staticmethod
    def get_google_config() -> dict:
        return {
            "CLIENT_ID": os.environ.get("GOOGLE_CLIENT_ID"),
            "CLIENT_SECRET": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "REDIRECT_URI": os.environ.get("GOOGLE_REDIRECT_URI"),
        }

    @staticmethod
    def get_auth0_config() -> dict:
        return {
            "CLIENT_ID": os.environ.get("AUTH0_CLIENT_ID"),
            "CLIENT_SECRET": os.environ.get("AUTH0_CLIENT_SECRET"),
            "REDIRECT_URI": os.environ.get("AUTH0_REDIRECT_URI"),
            "DOMAIN": os.environ.get("AUTH0_DOMAIN"),
        }

    # Add more identity provider configurations as needed

class IdentityClientHelper:
    """
    Provides general helper utilities for identity-related operations.
    """
    @staticmethod
    def generate_state() -> str:
        """
        Generates a secure random string for OAuth state parameter.
        """
        import secrets
        return secrets.token_urlsafe(32)
