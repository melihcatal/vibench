import os

import requests


PERSPECTIVE_HOST = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_api_key(config=None):
    config = config or {}
    return config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]


def post_perspective(payload, config=None, timeout=30):
    response = requests.post(PERSPECTIVE_HOST, params={"key": get_api_key(config)}, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()
