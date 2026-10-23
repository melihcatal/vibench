import os
import requests


def payload_safety(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    r = requests.post(
        f"{endpoint.rstrip('/')}/contentsafety/text:analyze?api-version=2023-10-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": text},
    )
    r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    payload_safety(os.environ.get("TEXT", ""))
