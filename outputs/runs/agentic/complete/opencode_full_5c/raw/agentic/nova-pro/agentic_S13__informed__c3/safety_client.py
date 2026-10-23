import os

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def get_client():
    return requests


def get_headers():
    return {"Content-Type": "application/json", "key": PERSPECTIVE_API_KEY}
