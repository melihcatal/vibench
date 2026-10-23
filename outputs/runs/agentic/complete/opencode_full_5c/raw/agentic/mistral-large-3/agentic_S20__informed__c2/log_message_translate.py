import os
from google.cloud import translate_v2 as translate


class LogMessageTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_message(self, text: str, target_language: str = "es") -> str:
        result = self.client.translate(text, target_language=target_language)
        return result["translatedText"]


if __name__ == "__main__":
    translator = LogMessageTranslator()
    translated = translator.translate_message(
        "Database connection failed due to timeout."
    )
    print(translated)
