import os

import requests

from safety_client import get_perspective_client


def embed_moderation_rationale(rationale):
    client = get_perspective_client()
    response = client.embed(rationale)
    return response['embedding']