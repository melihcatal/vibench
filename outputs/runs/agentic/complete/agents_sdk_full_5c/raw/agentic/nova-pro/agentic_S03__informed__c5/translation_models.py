from azure.ai.translation.text import TextTranslationInput

def create_translation_input(text, to_language):
    return TextTranslationInput(text=text, to=[to_language])
