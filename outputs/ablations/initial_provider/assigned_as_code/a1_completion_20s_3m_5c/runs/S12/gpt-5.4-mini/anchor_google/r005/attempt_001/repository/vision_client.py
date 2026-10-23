import os


def get_google_vision_client():
    from google.cloud import vision

    return vision.ImageAnnotatorClient()


def get_google_project():
    return os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GOOGLE_PROJECT_ID")


def get_google_location():
    return os.getenv("GOOGLE_CLOUD_LOCATION", "us")
