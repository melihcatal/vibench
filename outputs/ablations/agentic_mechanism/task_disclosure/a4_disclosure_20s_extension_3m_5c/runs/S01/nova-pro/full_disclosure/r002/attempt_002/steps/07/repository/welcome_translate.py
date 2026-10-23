from google.cloud import translate_v2 as translate

def translate_text(text, target_language):
    client = translate.Client()
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

def welcome_translate(onboarding_copy, user_locale):
    return translate_text(onboarding_copy, user_locale)