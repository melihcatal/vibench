import os

import deepl

from safety_models import ThresholdDecision


def translate_appeal_text(
    appeal_text: str,
    target_language: str = "EN-US",
    source_language: str | None = None,
    api_key: str | None = None,
) -> str:
    if api_key is None:
        api_key = os.environ.get("DEEPL_AUTH_KEY", "")

    translator = deepl.Translator(api_key)

    kwargs = {"target_lang": target_language}
    if source_language:
        kwargs["source_lang"] = source_language

    result = translator.translate_text(appeal_text, **kwargs)
    return result.text


def translate_appeal_for_decision(
    decision: ThresholdDecision,
    appeal_text: str,
    target_language: str = "EN-US",
    api_key: str | None = None,
) -> dict:
    translated = translate_appeal_text(appeal_text, target_language, api_key=api_key)

    violated = ", ".join(c.value for c in decision.violated_categories)

    return {
        "decision_id": id(decision),
        "original_appeal": appeal_text,
        "translated_appeal": translated,
        "target_language": target_language,
        "original_decision": {
            "allowed": decision.allowed,
            "violated_categories": violated,
        },
    }


def batch_translate_appeals(
    appeals: list[tuple[str, str]],
    target_language: str = "EN-US",
    api_key: str | None = None,
) -> list[dict]:
    if api_key is None:
        api_key = os.environ.get("DEEPL_AUTH_KEY", "")

    translator = deepl.Translator(api_key)

    texts = [appeal for _, appeal in appeals]
    results = translator.translate_text(texts, target_lang=target_language)

    translated_texts = [r.text for r in results]

    output = []
    for (decision_id, appeal), translated in zip(appeals, translated_texts):
        output.append(
            {
                "decision_id": decision_id,
                "original_appeal": appeal,
                "translated_appeal": translated,
                "target_language": target_language,
            }
        )

    return output
