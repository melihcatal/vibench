from google.cloud import translate_v2 as translate


def welcome_translate(onboarding_copy: str, target_locale: str) -> str:
    client = translate.Client()
    result = client.translate(onboarding_copy, target_language=target_locale)
    return result["translatedText"]
