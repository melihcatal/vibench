from model_client import ManagedModelClient


def localize_platform_output(output: str, target_locale: str) -> str:
    # Example: use Google Cloud Translate for demo purposes
    client = ManagedModelClient(provider="google-translate")
    localized = client.translate(text=output, target_locale=target_locale)
    return localized
