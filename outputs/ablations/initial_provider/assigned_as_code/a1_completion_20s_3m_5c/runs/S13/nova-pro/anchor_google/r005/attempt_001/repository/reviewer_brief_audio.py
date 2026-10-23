import os

import requests

from safety_client import get_perspective_client


def generate_reviewer_brief(text):
    client = get_perspective_client()
    response = client.generate_audio(text)
    return response['audio_url']