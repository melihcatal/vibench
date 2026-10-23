import os
import json
import deepl


def translate_payload(
    text: str,
    target_lang: str = "ES",
    source_lang: str = "EN",
) -> dict:
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    result = translator.translate_text(
        text,
        source_lang=source_lang,
        target_lang=target_lang,
    )

    return {
        "original_text": text,
        "translated_text": result.text,
        "source_lang": result.source_lang
        if hasattr(result, "source_lang")
        else source_lang,
        "target_lang": target_lang,
        "status": "translated",
        "provider": "DeepL API",
    }


def translate_payload_batch(
    texts: list[str],
    target_lang: str = "ES",
    source_lang: str = "EN",
) -> list[dict]:
    auth_key = os.getenv("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")

    translator = deepl.Translator(auth_key)

    results = translator.translate_text(
        texts,
        source_lang=source_lang,
        target_lang=target_lang,
    )

    output = []
    for idx, result in enumerate(results):
        output.append(
            {
                "original_text": texts[idx],
                "translated_text": result.text,
                "source_lang": result.source_lang
                if hasattr(result, "source_lang")
                else source_lang,
                "target_lang": target_lang,
                "status": "translated",
                "provider": "DeepL API",
            }
        )

    return output


if __name__ == "__main__":
    sample_text = "Your order has been confirmed and will ship within 2 business days."
    result = translate_payload(sample_text, target_lang="ES")
    print(json.dumps(result, indent=2))
