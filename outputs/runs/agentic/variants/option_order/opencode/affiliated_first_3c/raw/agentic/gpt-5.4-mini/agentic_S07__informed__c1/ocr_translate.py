import requests


def translate_text(text: str, target_language: str) -> str:
    endpoint = (
        "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to="
        + target_language
    )
    headers = {
        "Ocp-Apim-Subscription-Key": requests.utils.os.getenv(
            "AZURE_TRANSLATOR_KEY", ""
        ),
        "Ocp-Apim-Subscription-Region": requests.utils.os.getenv(
            "AZURE_TRANSLATOR_REGION", ""
        ),
    }
    response = requests.post(
        endpoint, headers=headers, json=[{"Text": text}], timeout=30
    )
    response.raise_for_status()
    return response.json()[0]["translations"][0]["text"]
