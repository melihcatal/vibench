import os
import sys

import requests


def visual_safety_text(text: str) -> dict:
    url = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    response = requests.post(
        url,
        params={"key": os.environ["PERSPECTIVE_API_KEY"]},
        json={"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print(visual_safety_text(sys.argv[1]))
