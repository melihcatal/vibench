import os


def load_image(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
