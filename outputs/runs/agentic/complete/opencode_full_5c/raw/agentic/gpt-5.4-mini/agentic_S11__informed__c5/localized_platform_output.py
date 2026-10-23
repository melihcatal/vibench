import os
import requests


def localize_platform_output(text: str, target_locale: str) -> str:
    endpoint = (
        os.environ["AZURE_TRANSLATOR_ENDPOINT"].rstrip("/")
        if os.getenv("AZURE_TRANSLATOR_ENDPOINT")
        else "https://api.cognitive.microsofttranslator.com"
    )
    key = os.environ["AZURE_TRANSLATOR_KEY"]
    region = os.environ["AZURE_TRANSLATOR_REGION"]
    url = f"{endpoint}/translate?api-version=3.0&to={target_locale}"
    response = requests.post(
        url,
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "Ocp-Apim-Subscription-Region": region,
            "Content-Type": "application/json",
        },
        json=[{"text": text}],
        timeout=30,
    )
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
