import os
import requests
from model_models import normalize_text


def check_platform_output_safety(text: str):
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    response = requests.post(
        f"{endpoint}/contentsafety/text:analyze?api-version=2024-09-01",
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"},
        json={"text": normalize_text(text)},
    )
    response.raise_for_status()
    return response.json()
