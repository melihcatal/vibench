import os
from typing import Optional
from security_models import ComplianceTranslation
from security_client import get_translate_client, load_aws_config


DEFAULT_SOURCE_LANGUAGE = "en"
DEFAULT_TARGET_LANGUAGE = "es"


def translate_compliance_note(
    text: str,
    source_language: str = None,
    target_language: str = None,
    terminology_names: list = None,
) -> ComplianceTranslation:
    config = load_aws_config()
    translate_client = get_translate_client(config)

    src_lang = source_language or os.environ.get(
        "AWS_TRANSLATE_SOURCE_LANG", DEFAULT_SOURCE_LANGUAGE
    )
    tgt_lang = target_language or os.environ.get(
        "AWS_TRANSLATE_TARGET_LANG", DEFAULT_TARGET_LANGUAGE
    )

    params = {
        "Text": text,
        "SourceLanguageCode": src_lang,
        "TargetLanguageCode": tgt_lang,
    }

    if terminology_names:
        params["TerminologyNames"] = terminology_names

    response = translate_client.translate_text(**params)

    translated_text = response.get("TranslatedText", "")

    return ComplianceTranslation(
        source_text=text,
        translated_text=translated_text,
        source_language=response.get("SourceLanguageCode", src_lang),
        target_language=response.get("TargetLanguageCode", tgt_lang),
        model_id="aws-translate-neural",
    )


def translate_batch_compliance_notes(
    texts: list,
    source_language: str = None,
    target_language: str = None,
) -> list:
    results = []
    for text in texts:
        result = translate_compliance_note(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )
        results.append(result)
    return results


def format_translation_output(translation: ComplianceTranslation) -> str:
    return (
        f"Translation (AWS Translate Neural)\n"
        f"Source ({translation.source_language}): {translation.source_text}\n"
        f"Target ({translation.target_language}): {translation.translated_text}\n"
        f"Model: {translation.model_id}"
    )


if __name__ == "__main__":
    note = "All encryption keys must be rotated every 90 days per SOC 2 compliance requirements."
    result = translate_compliance_note(note, target_language="es")
    print(format_translation_output(result))
