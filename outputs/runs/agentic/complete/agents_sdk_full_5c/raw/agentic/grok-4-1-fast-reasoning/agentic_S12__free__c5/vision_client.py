import os
import base64

def encode_image(image_path: str) -> str:
    """Encode local image file to base64 string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_openai_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return key

def get_anthropic_api_key() -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return key

def get_s3_bucket() -> str:
    bucket = os.getenv("AWS_S3_IMAGE_BUCKET")
    if not bucket:
        raise ValueError("AWS_S3_IMAGE_BUCKET environment variable is required")
    return bucket