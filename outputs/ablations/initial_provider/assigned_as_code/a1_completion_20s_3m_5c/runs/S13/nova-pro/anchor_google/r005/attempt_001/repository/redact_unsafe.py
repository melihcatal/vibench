import os

import requests

from safety_client import get_perspective_client
from safety_models import normalize_response


def redact_unsafe(text, config=None):
    client = get_perspective_client(config)
    response = client.analyze(text)
    if response['toxicity'] > 0.5:
        return 'REDACTED'
    return text