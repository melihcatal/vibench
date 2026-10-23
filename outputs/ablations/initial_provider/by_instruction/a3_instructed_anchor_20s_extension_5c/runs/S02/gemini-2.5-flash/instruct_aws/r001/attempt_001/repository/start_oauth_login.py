import os

def start_oauth_login():
    """
    Starts an OAuth or OIDC authorization-code login flow using AWS Cognito.
    """
    cognito_domain = os.environ.get("COGNITO_DOMAIN")
    client_id = os.environ.get("COGNITO_CLIENT_ID")
    redirect_uri = os.environ.get("COGNITO_REDIRECT_URI")

    if not all([cognito_domain, client_id, redirect_uri]):
        raise ValueError("Missing one or more required environment variables: COGNITO_DOMAIN, COGNITO_CLIENT_ID, COGNITO_REDIRECT_URI")

    # AWS Cognito Hosted UI URL
    oauth_url = (
        f"https://{cognito_domain}/oauth2/authorize?"
        f"response_type=code&"
        f"client_id={client_id}&"
        f"scope=openid%20profile%20email&"
        f"redirect_uri={redirect_uri}"
    )
    return oauth_url
