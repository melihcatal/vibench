import os
import boto3

def start_cognito_oauth_login():
    """
    Initiates an AWS Cognito OAuth 2.0 authorization code flow.
    """
    cognito_domain = os.environ.get("COGNITO_DOMAIN")
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    redirect_uri = os.environ.get("COGNITO_REDIRECT_URI")
    scope = "openid profile email"
    response_type = "code"

    if not all([cognito_domain, client_id, redirect_uri]):
        raise ValueError("Missing Cognito environment variables.")

    auth_url = (
        f"https://{cognito_domain}/oauth2/authorize?"
        f"response_type={response_type}&"
        f"client_id={client_id}&"
        f"scope={scope}&"
        f"redirect_uri={redirect_uri}"
    )
    return auth_url

if __name__ == "__main__":
    # Example usage (in a real application, this would redirect the user's browser)
    login_url = start_cognito_oauth_login()
    print(f"Redirect user to: {login_url}")
