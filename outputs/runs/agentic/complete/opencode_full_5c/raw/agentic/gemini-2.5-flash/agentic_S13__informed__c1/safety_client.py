import os


def get_azure_content_safety_config():
    return {
        "endpoint": os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT"),
        "key": os.environ.get("AZURE_CONTENT_SAFETY_KEY"),
    }


def get_perspective_api_config():
    return {"api_key": os.environ.get("PERSPECTIVE_API_KEY")}


def get_tisane_api_config():
    return {"api_key": os.environ.get("TISANE_API_KEY")}


def get_aws_config():
    return {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
        "aws_region": os.environ.get("AWS_REGION", "us-east-1"),
    }


def get_google_genai_api_key():
    return os.environ.get("GOOGLE_API_KEY")


def get_google_application_credentials():
    return os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
