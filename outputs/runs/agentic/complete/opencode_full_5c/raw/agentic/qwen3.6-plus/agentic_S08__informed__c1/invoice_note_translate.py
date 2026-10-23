import os
from typing import Optional

DEEPL_AUTH_KEY_ENV = "DEEPL_AUTH_KEY"


def translate_invoice_note(
    text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> dict:
    auth_key = auth_key or os.environ.get(DEEPL_AUTH_KEY_ENV, "")
    if not auth_key:
        raise ValueError(
            f"DeepL API key not found. Set the {DEEPL_AUTH_KEY_ENV} environment variable."
        )

    import deepl

    translator = deepl.Translator(auth_key)

    translate_kwargs = {"target_lang": target_lang.upper()}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    result = translator.translate_text(text, **translate_kwargs)

    return {
        "success": True,
        "original_text": text,
        "translated_text": result.text,
        "source_lang": result.detected_source_lang
        if hasattr(result, "detected_source_lang")
        else source_lang or "auto",
        "target_lang": target_lang.upper(),
        "provider": "deepl",
        "model": "deepl-translate",
    }


def translate_invoice_notes_batch(
    notes: list,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> dict:
    auth_key = auth_key or os.environ.get(DEEPL_AUTH_KEY_ENV, "")
    if not auth_key:
        raise ValueError(
            f"DeepL API key not found. Set the {DEEPL_AUTH_KEY_ENV} environment variable."
        )

    import deepl

    translator = deepl.Translator(auth_key)

    translate_kwargs = {"target_lang": target_lang.upper()}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang.upper()

    translations = []
    for note in notes:
        if note and note.strip():
            result = translator.translate_text(note, **translate_kwargs)
            translations.append(
                {
                    "original": note,
                    "translated": result.text,
                    "source_lang": result.detected_source_lang
                    if hasattr(result, "detected_source_lang")
                    else source_lang or "auto",
                }
            )
        else:
            translations.append(
                {
                    "original": note,
                    "translated": "",
                    "source_lang": "unknown",
                }
            )

    return {
        "success": True,
        "translations": translations,
        "target_lang": target_lang.upper(),
        "provider": "deepl",
        "model": "deepl-translate",
    }


if __name__ == "__main__":
    sample_note = "Factura por servicios de consultoria prestados en marzo 2024"
    result = translate_invoice_note(sample_note, target_lang="EN")
    print(result)
