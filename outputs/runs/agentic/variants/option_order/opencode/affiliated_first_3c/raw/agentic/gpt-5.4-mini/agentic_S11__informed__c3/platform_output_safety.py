import requests
from model_models import PlatformResponse


def platform_output_safety(response: PlatformResponse) -> dict:
    endpoint = "https://api.content-safety.azure.com/text:analyze"
    payload = {"text": response.text, "categories": ["Hate", "Violence", "SelfHarm", "Sexual"]}
    return requests.post(endpoint, headers={"Ocp-Apim-Subscription-Key": __import__("os").environ["AZURE_CONTENT_SAFETY_KEY"]}, json=payload, timeout=30).json()
