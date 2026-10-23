import os
import deepl

def translate_text_segments(segments: list[str], target_lang: str = "DE") -> list[str]:
    """
    Translates a list of text segments using the DeepL API.

    Args:
        segments: A list of strings to translate.
        target_lang: The target language code (e.g., "DE" for German).

    Returns:
        A list of translated strings.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(segments, target_lang=target_lang)
        
        if isinstance(result, list):
            return [translation.text for translation in result]
        else: # handles single text input
            return [result.text]

    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return []

if __name__ == '__main__':
    sample_texts = [
        "Hello, world!",
        "This is a test of the translation service."
    ]
    
    translated_texts = translate_text_segments(sample_texts, "ES") # Translate to Spanish
    
    if translated_texts:
        print("Original vs. Translated:")
        for original, translated in zip(sample_texts, translated_texts):
            print(f'"{original}" -> "{translated}"')
