import requests


def unsafe_copy_check(text: str) -> dict:
    response = requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": "", "text": text},
    )
    return response.json()
