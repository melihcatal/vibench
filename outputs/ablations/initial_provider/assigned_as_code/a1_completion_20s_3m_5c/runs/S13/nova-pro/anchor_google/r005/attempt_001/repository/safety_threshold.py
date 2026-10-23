import os

import requests

from safety_client import get_perspective_client
from safety_models import normalize_response


def apply_safety_threshold(text, threshold=0.5, config=None):
    client = get_perspective_client(config)
    response = client.analyze(text)
    if response['toxicity'] > threshold:
        return False
    return True