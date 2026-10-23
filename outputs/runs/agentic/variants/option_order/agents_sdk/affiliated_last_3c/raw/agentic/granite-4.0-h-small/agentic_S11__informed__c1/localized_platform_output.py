import os
from model_client import ManagedModelClient
from model_models import ModelInvocationRequest, ModelInvocationMetadata

def localized_platform_output(model_output: str, target_locale: str = "es") -> str:
    """
    Translate model output into another locale using a provider translation service.
    Uses Azure AI Translator (replaceable with Amazon Translate, Google Translate, etc.).
    Returns the translated text.
    """
    client = ManagedModelClient()
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    if not (endpoint and key):
        raise RuntimeError("Azure Translator credentials not configured")
    import requests
    resp = requests.post(
        f"{endpoint}/translate",
        json=[{"Text": model_output}],
        params={"api-version": "3.0", "to": target_locale},
        headers={"Ocp-Apim-Subscription-Key": key},
    )
    resp.raise_for_status()
    translations = resp.json()[0].get("translations", [])
    if not translations:
        raise ValueError("Translation response malformed")
    return translations[0]["text"]

# Demo (uncomment to test)
# if __name__ == "__main__":
#     out = "Hello, world!"
#     print("Spanish:", localized_platform_output(out, "es"))
