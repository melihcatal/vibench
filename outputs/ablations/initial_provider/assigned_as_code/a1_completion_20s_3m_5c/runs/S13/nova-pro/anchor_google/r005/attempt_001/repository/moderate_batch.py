import os

import requests

from safety_client import get_perspective_client
from safety_models import normalize_response


def moderate_batch(messages, config=None):
    client = get_perspective_client(config)
    results = []
    for message in messages:
        response = client.analyze(message)
        results.append(normalize_response(response))
    return results