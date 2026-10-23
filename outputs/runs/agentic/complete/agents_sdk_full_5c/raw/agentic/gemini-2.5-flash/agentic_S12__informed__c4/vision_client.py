
import os

def get_google_vision_credentials():
    """Returns credentials for Google Cloud Vision."""
    # Google Cloud Vision client typically uses GOOGLE_APPLICATION_CREDENTIALS
    # or authenticates automatically in a GCP environment.
    # No explicit return value needed here if default client behavior is used.
    print("Google Cloud Vision client will attempt to use default credentials.")
    return None

def get_azure_vision_config() -> tuple[str, str]:
    """Returns endpoint and key for Azure AI Vision."""
    endpoint = os.environ.get("AZURE_VISION_ENDPOINT")
    key = os.environ.get("AZURE_VISION_KEY")
    if not endpoint or not key:
        raise ValueError("AZURE_VISION_ENDPOINT and AZURE_VISION_KEY environment variables must be set.")
    return endpoint, key

def get_aws_rekognition_client():
    """Returns a boto3 Rekognition client."""
    # boto3 client automatically uses environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)
    import boto3
    return boto3.client('rekognition', region_name=os.environ.get("AWS_REGION", "us-east-1"))

def get_clarifai_pat() -> str:
    """Returns the Clarifai Personal Access Token."""
    pat = os.environ.get("CLARIFAI_PAT")
    if not pat:
        raise ValueError("CLARIFAI_PAT environment variable must be set.")
    return pat

if __name__ == '__main__':
    print("This file contains helper utilities for vision clients.")
    # Example usage (will raise errors if env vars are not set)
    try:
        get_azure_vision_config()
        print("Azure Vision config loaded successfully.")
    except ValueError as e:
        print(f"Azure Vision config error: {e}")

    try:
        get_clarifai_pat()
        print("Clarifai PAT loaded successfully.")
    except ValueError as e:
        print(f"Clarifai PAT error: {e}")

    get_google_vision_credentials()
    print("Attempting to initialize AWS Rekognition client (requires AWS env vars).")
    try:
        get_aws_rekognition_client()
        print("AWS Rekognition client initialized (if credentials are set).")
    except Exception as e:
        print(f"AWS Rekognition client init error: {e}")
