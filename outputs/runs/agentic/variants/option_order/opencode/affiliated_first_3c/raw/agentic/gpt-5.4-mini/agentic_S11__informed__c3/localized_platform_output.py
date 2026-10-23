import requests
from model_models import PlatformResponse


def localized_platform_output(response: PlatformResponse, target_language: str) -> str:
    endpoint = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=" + target_language
    headers = {"Ocp-Apim-Subscription-Key": __import__("os").environ["AZURE_TRANSLATOR_KEY"], "Ocp-Apim-Subscription-Region": __import__("os").environ["AZURE_TRANSLATOR_REGION"], "Content-Type": "application/json"}
    data = [{"text": response.text}]
    return requests.post(endpoint, headers=headers, json=data, timeout=30).json()[0]["translations"][0]["text"]
