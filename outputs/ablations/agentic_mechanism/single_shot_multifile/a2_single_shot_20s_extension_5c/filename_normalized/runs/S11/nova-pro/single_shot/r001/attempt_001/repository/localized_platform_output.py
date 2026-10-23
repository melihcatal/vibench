import os
from model_client import get_platform_client

def translate_output(output_text, target_language):
    client = get_platform_client()
    translated_text = client.translate_text(output_text, target_language)
    return translated_text