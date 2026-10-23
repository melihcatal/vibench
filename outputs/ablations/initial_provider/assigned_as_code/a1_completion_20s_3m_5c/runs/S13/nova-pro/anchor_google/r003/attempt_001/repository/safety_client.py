import requests


def get_safety_client(config=None):
    return requests.Session()