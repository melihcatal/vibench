import os
import requests


def get_client():
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    return requests.Session()


def get_headers():
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    return {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
