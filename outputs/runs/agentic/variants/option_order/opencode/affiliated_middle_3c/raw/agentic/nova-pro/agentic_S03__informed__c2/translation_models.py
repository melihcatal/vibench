from azure.ai.translation.text.models import TextTranslationInput


def create_translation_request(texts, from_language, to_language):
    return [
        TextTranslationInput(
            text=text, from_language=from_language, to_language=to_language
        )
        for text in texts
    ]
