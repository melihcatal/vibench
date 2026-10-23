import deeptranslator
from translation_models import SupportedModels


class BatchTranslator:
    def __init__(self, source_lang: str = "EN"):
        self.source_lang = source_lang
        self.translator = deeptranslator.DeepL(auth_key=SupportedModels.DeeplAuthKey)

    def translate(self, texts: list[str]) -> list[str]:
        """Translate a list of strings while preserving order."""
        return [
            self.translator.translate(translation=self.translator.translate(text=text))
            for text in texts
        ]


if __name__ == "__main__":
    translator = BatchTranslator()
    translations = translator.translate(["Hello", "Hi", "Hey"])
    print(translations)
