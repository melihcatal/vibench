from azure.ai.translation.text import TextTranslationInput

def create_translation_input(texts, to_language):
    return TextTranslationInput(text=texts, to=[to_language] * len(texts))