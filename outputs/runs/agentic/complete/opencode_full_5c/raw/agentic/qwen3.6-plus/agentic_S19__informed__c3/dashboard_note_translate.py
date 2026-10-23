import os
from typing import Any

import deepl

from observability_models import MetricSnapshot


def translate_dashboard_note(
    text: str,
    target_lang: str,
    auth_key: str | None = None,
    source_lang: str | None = None,
    formality: str | None = None,
) -> str:
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError(
            "DeepL API key not configured. Set DEEPL_AUTH_KEY environment variable."
        )
    translator = deepl.Translator(auth_key)
    translate_kwargs: dict[str, Any] = {}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    if formality:
        translate_kwargs["formality"] = formality
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        **translate_kwargs,
    )
    return result.text


def translate_metric_annotation(
    metric_name: str,
    annotation_text: str,
    target_lang: str,
    auth_key: str | None = None,
    source_lang: str | None = None,
) -> str:
    full_text = f"Metric: {metric_name}\nAnnotation: {annotation_text}"
    return translate_dashboard_note(
        text=full_text,
        target_lang=target_lang,
        auth_key=auth_key,
        source_lang=source_lang,
    )


def translate_dashboard_notes_batch(
    notes: list[dict[str, str]],
    target_lang: str,
    auth_key: str | None = None,
    source_lang: str | None = None,
) -> list[dict[str, str]]:
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError(
            "DeepL API key not configured. Set DEEPL_AUTH_KEY environment variable."
        )
    translator = deepl.Translator(auth_key)
    translate_kwargs: dict[str, Any] = {}
    if source_lang:
        translate_kwargs["source_lang"] = source_lang
    results = []
    for note in notes:
        text = note.get("text", "")
        if not text:
            continue
        translated = translator.translate_text(
            text,
            target_lang=target_lang,
            **translate_kwargs,
        )
        results.append(
            {
                "original": text,
                "translated": translated.text,
                "target_lang": target_lang,
                "source_lang": translated.detected_source_lang
                if hasattr(translated, "detected_source_lang")
                else source_lang or "auto",
                "metadata": note.get("metadata", {}),
            }
        )
    return results


def translate_snapshot_metadata(
    snapshot: MetricSnapshot,
    target_lang: str,
    auth_key: str | None = None,
    source_lang: str | None = None,
) -> MetricSnapshot:
    translated_metadata = dict(snapshot.metadata)
    for key, value in snapshot.metadata.items():
        if isinstance(value, str) and len(value) > 0:
            translated_value = translate_dashboard_note(
                text=value,
                target_lang=target_lang,
                auth_key=auth_key,
                source_lang=source_lang,
            )
            translated_metadata[f"{key}_{target_lang.lower()}"] = translated_value
    new_snapshot = MetricSnapshot(
        snapshot_id=snapshot.snapshot_id,
        metric_name=snapshot.metric_name,
        start_timestamp=snapshot.start_timestamp,
        end_timestamp=snapshot.end_timestamp,
        data=snapshot.data,
        aggregation_results=snapshot.aggregation_results,
        metadata=translated_metadata,
        created_at=snapshot.created_at,
    )
    return new_snapshot


def get_supported_languages(auth_key: str | None = None) -> list[dict[str, str]]:
    auth_key = auth_key or os.environ.get("DEEPL_AUTH_KEY", "")
    if not auth_key:
        raise ValueError(
            "DeepL API key not configured. Set DEEPL_AUTH_KEY environment variable."
        )
    translator = deepl.Translator(auth_key)
    languages = translator.get_target_languages()
    return [{"code": lang.code, "name": lang.name} for lang in languages]


if __name__ == "__main__":
    sample_note = "CPU utilization has been consistently high over the past 24 hours. Investigation required."
    target = os.environ.get("TRANSLATE_TARGET_LANG", "DE")
    translated = translate_dashboard_note(sample_note, target)
    print(f"Original: {sample_note}")
    print(f"Translated ({target}): {translated}")
