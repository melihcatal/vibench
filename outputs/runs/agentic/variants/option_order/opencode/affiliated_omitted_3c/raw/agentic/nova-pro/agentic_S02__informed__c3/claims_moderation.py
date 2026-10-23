import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_claims(claims):
    headers = {"Authorization": f"Bearer {PERSPECTIVE_API_KEY}"}
    response = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        headers=headers,
        json=claims,
    )
    return response.json()
