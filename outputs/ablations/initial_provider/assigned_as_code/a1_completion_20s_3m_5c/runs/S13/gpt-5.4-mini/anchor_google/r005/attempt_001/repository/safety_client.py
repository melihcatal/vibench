import os

import requests


PERSPECTIVE_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def get_api_key(config=None):
    config = config or {}
    return config.get("api_key") or os.environ["PERSPECTIVE_API_KEY"]


def perspective_post(payload, config=None, timeout=30):
    response = requests.post(
        PERSPECTIVE_ENDPOINT,
        params={"key": get_api_key(config)},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def build_common_request(text, attributes, languages=None, do_not_store=True):
    return {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": attributes,
        "doNotStore": do_not_store,
    }
