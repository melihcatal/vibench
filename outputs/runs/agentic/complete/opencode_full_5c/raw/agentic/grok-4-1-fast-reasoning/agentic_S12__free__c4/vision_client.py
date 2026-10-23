import os
import base64
import io

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET")
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


def load_image_bytes(image_path: str) -> bytes:
    with io.open(image_path, "rb") as f:
        return f.read()


def image_b64(image_path: str) -> str:
    content = load_image_bytes(image_path)
    return base64.b64encode(content).decode("utf-8")
