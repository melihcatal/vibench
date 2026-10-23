import os

import requests


def main() -> None:
    requests.post(
        "https://api.perspectiveapi.com/v1alpha1/comments:analyze",
        params={"key": os.environ.get("PERSPECTIVE_API_KEY", "")},
        json={
            "comment": {"text": "sample log text"},
            "requestedAttributes": {"TOXICITY": {}},
        },
        timeout=30,
    )


if __name__ == "__main__":
    main()
