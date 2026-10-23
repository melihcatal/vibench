import os


def get_cognito_config():
    return {
        "user_pool_id": os.environ["COGNITO_USER_POOL_ID"],
        "app_client_id": os.environ["COGNITO_APP_CLIENT_ID"],
        "region": os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        "aws_access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
        "aws_secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
    }
