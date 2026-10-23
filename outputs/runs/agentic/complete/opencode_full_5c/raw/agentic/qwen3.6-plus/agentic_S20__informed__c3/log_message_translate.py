import os

import deepl

DEEPL_AUTH_KEY = os.environ["DEEPL_AUTH_KEY"]


def translate_log_message(text: str, target_lang: str = "ES") -> str:
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        preserve_formatting=True,
    )
    return result.text


def translate_log_messages(messages: list[str], target_lang: str = "ES") -> list[dict]:
    if not messages:
        return []
    translator = deepl.Translator(DEEPL_AUTH_KEY)
    texts = [deepl.Text(msg, preserve_formatting=True) for msg in messages]
    results = translator.translate_text(
        texts,
        target_lang=target_lang,
    )
    translations = []
    for original, translated in zip(messages, results):
        translations.append(
            {
                "original": original,
                "translated": translated.text,
                "target_lang": target_lang,
            }
        )
    return translations


if __name__ == "__main__":
    sample_messages = [
        "Database connection pool exhausted",
        "Request timeout after 30 seconds",
        "Circuit breaker opened for downstream service",
    ]
    translated = translate_log_messages(sample_messages, target_lang="ES")
    for item in translated:
        print(item)
