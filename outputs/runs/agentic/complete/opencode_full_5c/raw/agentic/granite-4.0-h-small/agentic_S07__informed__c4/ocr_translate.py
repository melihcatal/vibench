import os
from google.cloud import translate_v2 as translate

# Use environment variable for Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/google-credentials.json"


class GoogleTranslateClient:
    def __init__(self):
        self.client = translate.Client()

    def translate_text(self, text: str, target_language: str = "en") -> str:
        """Translate extracted OCR text using Google Cloud Translate."""
        response = self.client.translate(text, target_language=target_language)
        return response["translatedText"]


def main():
    helper = GoogleTranslateClient()
    # Example usage with previously extracted text
    extracted_text = "This is a sample document in French."
    translated = helper.translate_text(extracted_text, target_language="en")
    print("Translated text:", translated)


if __name__ == "__main__":
    main()
