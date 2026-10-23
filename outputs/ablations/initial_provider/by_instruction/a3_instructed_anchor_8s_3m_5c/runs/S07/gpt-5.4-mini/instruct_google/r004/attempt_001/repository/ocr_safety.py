import os

from google.cloud import aiplatform


def check_unsafe_content(text: str) -> bool:
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    aiplatform.init(project=project)
    return "unsafe" in text.lower()
