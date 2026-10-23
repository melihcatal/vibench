import os

from googleapiclient.discovery import build


def get_perspective_client():
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    return build("commentanalyzer", "v1alpha1", developerKey=api_key)