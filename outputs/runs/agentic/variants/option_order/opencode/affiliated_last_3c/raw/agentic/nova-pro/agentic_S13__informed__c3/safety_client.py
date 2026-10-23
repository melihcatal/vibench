import os

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def get_client():
    return requests.Session()


def get_api_key():
    return PERSPECTIVE_API_KEY
