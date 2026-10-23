import deepl

DEEPL_TARGET_LANG = "EN"


def appeal_translate(
    appeal_text: str,
    target_lang: str = DEEPL_TARGET_LANG,
    auth_key: str | None = None,
    source_lang: str | None = None,
) -> dict:
    translator = deepl.Translator(auth_key)
    translate_kwargs: dict = {}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    result = translator.translate_text(
        appeal_text,
        target_lang=target_lang,
        **translate_kwargs,
    )
    return {
        "original_text": appeal_text,
        "translated_text": result.text,
        "source_lang": result.detected_source_lang or source_lang or "unknown",
        "target_lang": target_lang,
        "provider": "DeepL",
    }


def translate_appeals_batch(
    appeals: list[dict[str, str]],
    target_lang: str = DEEPL_TARGET_LANG,
    auth_key: str | None = None,
) -> list[dict]:
    translator = deepl.Translator(auth_key)
    texts = [a["text"] for a in appeals]
    results = translator.translate_text(
        texts,
        target_lang=target_lang,
    )
    output = []
    for i, appeal in enumerate(appeals):
        translated = results[i] if isinstance(results, list) else results
        output.append(
            {
                "appeal_id": appeal.get("id", i),
                "original_text": appeal["text"],
                "translated_text": translated.text
                if isinstance(translated, deepl.Text)
                else translated,
                "source_lang": translated.detected_source_lang
                if isinstance(translated, deepl.Text)
                else "unknown",
                "target_lang": target_lang,
            }
        )
    return output
