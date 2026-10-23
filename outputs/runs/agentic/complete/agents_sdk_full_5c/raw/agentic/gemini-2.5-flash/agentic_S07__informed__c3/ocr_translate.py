import os
from google.cloud import translate_v2 as translate

def translate_text(text: str, target_language: str = "en") -> str:
    """
    Translates the input text using Google Cloud Translation.
    """
    client = translate.Client()
    
    result = client.translate(text, target_language=target_language)
    
    return result["translatedText"]

if __name__ == '__main__':
    # Placeholder for direct execution
    # original_text = "Hallo Welt"
    # translated = translate_text(original_text, target_language="en")
    # print(f"Original: {original_text}, Translated: {translated}")
    pass
