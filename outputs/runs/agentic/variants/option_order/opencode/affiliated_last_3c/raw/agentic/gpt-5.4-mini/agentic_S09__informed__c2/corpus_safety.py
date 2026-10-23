import os

import requests


def corpus_safety(texts):
    api_key = os.environ.get("PERSPECTIVE_API_KEY", "")
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    return {
        "provider": "perspective",
        "checked": len(list(texts)),
        "endpoint": url,
        "has_key": bool(api_key),
    }
