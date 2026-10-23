import os

import requests


def get_safety_client(config=None):
    config = config or {}
    api_key = config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]
    return requests.Session()


def normalize_response(response):
    return response.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]