from deep_translator import DeeplTranslator


def translate_log_message(text: str, target_language: str) -> str:
    return DeeplTranslator(source="auto", target=target_language).translate(text)


if __name__ == "__main__":
    translate_log_message("sample log message", "fr")
