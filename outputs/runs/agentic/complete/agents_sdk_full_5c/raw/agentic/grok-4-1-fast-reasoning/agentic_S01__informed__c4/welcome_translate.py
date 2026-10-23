from google.cloud import translate_v2 as translate

def welcome_translate(onboarding_copy: str, locale: str):
    client = translate.Client()
    result = client.translate(onboarding_copy, target_language=locale)
    return result["translatedText"]