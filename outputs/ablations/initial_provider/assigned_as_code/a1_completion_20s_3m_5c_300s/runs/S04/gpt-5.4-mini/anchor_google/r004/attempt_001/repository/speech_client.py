import os

from google.cloud import speech


def get_client(config=None):
    config = config or {}
    client_options = config.get("client_options")
    if client_options:
        return speech.SpeechClient(client_options=client_options)
    return speech.SpeechClient()


def get_project_id(config=None):
    config = config or {}
    return config.get("project_id") or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")


def get_location(config=None):
    config = config or {}
    return config.get("location") or os.getenv("GOOGLE_CLOUD_LOCATION") or "global"
