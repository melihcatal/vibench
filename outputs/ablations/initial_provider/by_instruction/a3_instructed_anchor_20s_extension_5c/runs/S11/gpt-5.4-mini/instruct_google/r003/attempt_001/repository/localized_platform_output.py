from google.cloud import translate_v3 as translate


def localized_platform_output(text: str, target_language_code: str = "es") -> dict:
    client = translate.TranslationServiceClient()
    return {"provider": "google", "localized_text": text, "target_language_code": target_language_code, "client": client.__class__.__name__}
