import os
from google.cloud import translate_v2 as translate

class LiveCaptionTranslator:
    """Translates live captions using Google Cloud Translation."""
    def __init__(self, target_language: str = "es"):
        self.client = translate.Client()
        self.target_language = target_language
        print(f"Google Cloud Translation client initialized for target language: {target_language}")
        if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
            print("Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")

    def translate_caption(self, text: str) -> str:
        """Translates a single caption text string."""
        if not text.strip():
            return ""
        try:
            result = self.client.translate(text, target_language=self.target_language)
            translated_text = result['translatedText']
            # print(f"Original: \'{text}\' -> Translated ({self.target_language}): \'{translated_text}\'")
            return translated_text
        except Exception as e:
            print(f"Error during translation: {e}")
            return f"[Translation Error: {e}]"

    def __call__(self, text: str) -> str:
        return self.translate_caption(text)

if __name__ == "__main__":
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    else:
        print("Demonstrating live caption translation.")
        translator = LiveCaptionTranslator(target_language="fr")

        captions = [
            "Hello, how are you doing today?",
            "This is an example of a live transcript that needs translation.",
            "", # Empty string test
            "Goodbye for now."
        ]

        for caption in captions:
            translated = translator.translate_caption(caption)
            print(f"Original: \'{caption}\' | Translated (fr): \'{translated}\'")

        print("\nChanging target language to German.")
        translator_de = LiveCaptionTranslator(target_language="de")
        for caption in captions:
            translated = translator_de(caption)
            print(f"Original: \'{caption}\' | Translated (de): \'{translated}\'")
