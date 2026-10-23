import os
import openai
from document_client import DocumentClient
from document_models import TranslateTextRequest, TranslateTextResponse


class TranslateText:
    def __init__(self):
        # OpenAI client initialized with API key from environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.document_client = DocumentClient()

    def translate(
        self, source_text: str, target_lang: str = "es"
    ) -> TranslateTextResponse:
        """Translate extracted OCR text using OpenAI's GPT-4o model.

        Args:
            source_text: Text to be translated.
            target_lang: Target language code (default 'es' for Spanish).

        Returns:
            TranslateTextResponse with the translated text.
        """
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the following text into {target_lang}:",
                    "content": source_text,
                }
            ],
        )
        translated = response.choices[0].message.content
        return TranslateTextResponse(translation=translated)


if __name__ == "__main__":
    translator = TranslateText()
    result = translator.translate("Hello, world!", "fr")
    print(result.translation)
