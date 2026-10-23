import os

import requests

from safety_client import get_perspective_client


def translate_appeal(text, target_language='en'):
    client = get_perspective_client()
    response = client.translate(text, target_language)
    return response['translatedText']