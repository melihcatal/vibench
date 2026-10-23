import os
from google.cloud import translate_v2 as translate

def translate_caption_chunk(text: str, target_language: str = 'es') -> str:
    translate_client = translate.Client()

    if not isinstance(text, bytes):
        text = text.encode('utf-8')

    # Text can also be a sequence of strings, in which case this method
    # will return a list of concurrent translations.
    response = translate_client.translate(text, target_language=target_language)

    # The response is a dictionary with translatedText, detectedSourceLanguage, and input
    translated_text = response['translatedText']
    source_language = response['detectedSourceLanguage']

    print(f"Original ({source_language}): {text.decode('utf-8')}")
    print(f"Translated ({target_language}): {translated_text}")

    return translated_text

if __name__ == "__main__":
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    # Or use ADC:
    # from google.auth import default
    # credentials, project = default()

    example_caption = "Hello, how are you doing today? This is a test caption."
    translated = translate_caption_chunk(example_caption, target_language='fr')
    print(f"Translation result: {translated}")

    example_caption_zh = "你好，今天过得怎么样？这是一个测试字幕。"
    translated_en = translate_caption_chunk(example_caption_zh, target_language='en')
    print(f"Translation result: {translated_en}")
