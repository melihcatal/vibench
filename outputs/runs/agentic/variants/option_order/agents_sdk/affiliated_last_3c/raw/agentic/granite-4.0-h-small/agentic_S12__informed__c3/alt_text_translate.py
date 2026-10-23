import os
from google.cloud import translate_v2 as translate

def alt_text_translate(image_descriptions, target='es'):
    """Translate generated image descriptions using Google Cloud Translation."""
    client = translate.Client()
    translated = []
    for text in image_descriptions:
        translation = client.translate(text, target_language=target)
        translated.append(translation['translatedText'])
    return translated
