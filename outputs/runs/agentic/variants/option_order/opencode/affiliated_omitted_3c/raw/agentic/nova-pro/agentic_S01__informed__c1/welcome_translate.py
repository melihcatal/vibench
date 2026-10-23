from alibabacloud_alimt import Client as TranslationClient


def translate_onboarding_copy(text, target_language):
    client = TranslationClient(
        access_key_id="your_access_key_id", access_key_secret="your_access_key_secret"
    )
    response = client.translate(text, target_language)
    return response.translated_text
