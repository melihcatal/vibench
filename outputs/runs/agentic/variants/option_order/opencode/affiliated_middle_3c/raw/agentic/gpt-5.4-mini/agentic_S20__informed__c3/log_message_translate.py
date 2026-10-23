from deep_translator import GoogleTranslator


def main(text: str, target_language: str = "es") -> str:
    return GoogleTranslator(source="auto", target=target_language).translate(text)
