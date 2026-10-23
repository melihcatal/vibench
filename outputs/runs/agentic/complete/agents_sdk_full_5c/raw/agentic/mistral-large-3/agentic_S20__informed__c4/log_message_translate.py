import os
from google.cloud import translate_v2 as translate


class LogMessageTranslator:
    def __init__(self):
        self.client = translate.Client()

    def translate_message(self, message: str, target_language: str = "es") -> str:
        result = self.client.translate(
            message,
            target_language=target_language
        )
        return result["translatedText"]


if __name__ == "__main__":
    translator = LogMessageTranslator()
    translated = translator.translate_message("Service started successfully.")
    print(translated)