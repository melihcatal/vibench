import os

def get_cognito_config():
    """
    Loads and returns Cognito configuration from environment variables.
    """
    config = {
        "COGNITO_DOMAIN": os.environ.get("COGNITO_DOMAIN"),
        "COGNITO_USER_POOL_CLIENT_ID": os.environ.get("COGNITO_USER_POOL_CLIENT_ID"),
        "COGNITO_USER_POOL_CLIENT_SECRET": os.environ.get("COGNITO_USER_POOL_CLIENT_SECRET"),
        "COGNITO_REDIRECT_URI": os.environ.get("COGNITO_REDIRECT_URI"),
        "COGNITO_REGION": os.environ.get("COGNITO_REGION", "us-east-1"),
    }
    if not all([config["COGNITO_DOMAIN"], config["COGNITO_USER_POOL_CLIENT_ID"], config["COGNITO_REDIRECT_URI"]]):
        raise ValueError("Missing one or more required Cognito environment variables.")
    return config

def get_aws_region():
    """
    Returns the AWS region from environment variables, defaulting to 'us-east-1'.
    """
    return os.environ.get("AWS_REGION", "us-east-1")

