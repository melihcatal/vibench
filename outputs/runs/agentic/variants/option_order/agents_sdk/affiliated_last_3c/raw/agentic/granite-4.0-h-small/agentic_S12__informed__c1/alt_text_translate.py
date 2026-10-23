import os
import boto3
from google.cloud import translate_v2 as translate
from vision_models import normalize_text

# Google Cloud Translation client
client = translate.Client()

def alt_text_translate(source_text, target_lang='es'):
    """Translate plain text alt-description to another language."""
    result = client.translate(source_text, target_language=target_lang)
    translated = result['translatedText']
    return translated


def translate_image_descriptions(descriptions, target_lang='es'):
    """Translate a list of image captions."""
    translated = [alt_text_translate(txt, target_lang) for txt in descriptions]
    return normalize_text(translated)
