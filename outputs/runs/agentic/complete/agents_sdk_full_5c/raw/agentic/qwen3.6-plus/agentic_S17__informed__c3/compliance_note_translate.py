"""
[LATER-STEP] compliance_note_translate.py - Translate encryption or compliance notes for reviewers.

Provider: DeepL API
SDK: deepl
Auth: DEEPL_AUTH_KEY
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from typing import Any, Dict, List, Optional

import deepl

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s: %(message)s")

DEEPL_DEFAULT_TARGET_LANG = "EN-US"
DEEPL_SOURCE_LANG_AUTO = "auto"

COMPLIANCE_COMMON_LANGS = {
    "en": "EN-US",
    "de": "DE",
    "fr": "FR",
    "es": "ES",
    "pt": "PT-BR",
    "ja": "JA",
    "zh": "ZH",
    "it": "IT",
    "nl": "NL",
    "pl": "PL",
    "ru": "RU",
}


def translate_compliance_note(
    text: str,
    target_language: str = DEEPL_DEFAULT_TARGET_LANG,
    source_language: Optional[str] = DEEPL_SOURCE_LANG_AUTO,
    api_key: Optional[str] = None,
    formality: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Translate a single compliance or encryption note using the DeepL API.

    Provider: DeepL API
    SDK: deepl
    Auth: DEEPL_AUTH_KEY
    """
    deepl_api_key = api_key or os.environ.get("DEEPL_AUTH_KEY", "")
    if not deepl_api_key:
        raise ValueError(
            "DeepL API key is required. Set DEEPL_AUTH_KEY env var or pass --api-key."
        )

    translator = deepl.Translator(deepl_api_key)

    kwargs: Dict[str, Any] = {
        "target_lang": target_language,
    }
    if source_language and source_language != DEEPL_SOURCE_LANG_AUTO:
        kwargs["source_lang"] = source_language
    if formality:
        kwargs["formality"] = formality

    result = translator.translate_text(text, **kwargs)

    translated_text = result.text
    detected_source = result.detected_source_lang

    logger.info(
        "Translated compliance note from %s to %s (DeepL)",
        detected_source,
        target_language,
    )

    return {
        "original_text": text,
        "translated_text": translated_text,
        "detected_source_language": detected_source,
        "target_language": target_language,
        "formality": formality,
    }


def translate_compliance_notes_batch(
    notes: List[Dict[str, str]],
    target_language: str = DEEPL_DEFAULT_TARGET_LANG,
    source_language: Optional[str] = DEEPL_SOURCE_LANG_AUTO,
    api_key: Optional[str] = None,
    text_field: str = "text",
    formality: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Translate a batch of compliance or encryption notes using the DeepL API.

    Provider: DeepL API
    SDK: deepl
    Auth: DEEPL_AUTH_KEY
    """
    deepl_api_key = api_key or os.environ.get("DEEPL_AUTH_KEY", "")
    if not deepl_api_key:
        raise ValueError(
            "DeepL API key is required. Set DEEPL_AUTH_KEY env var or pass --api-key."
        )

    translator = deepl.Translator(deepl_api_key)

    texts = [note.get(text_field, "") for note in notes]

    kwargs: Dict[str, Any] = {
        "target_lang": target_language,
    }
    if source_language and source_language != DEEPL_SOURCE_LANG_AUTO:
        kwargs["source_lang"] = source_language
    if formality:
        kwargs["formality"] = formality

    results = translator.translate_text(texts, **kwargs)

    if not isinstance(results, list):
        results = [results]

    translated_notes = []
    for i, (note, result) in enumerate(zip(notes, results)):
        translated_note = {
            **note,
            "translated_text": result.text,
            "detected_source_language": result.detected_source_lang,
            "target_language": target_language,
            "original_field": text_field,
        }
        translated_notes.append(translated_note)

    logger.info(
        "Translated %d compliance notes to %s using DeepL API",
        len(translated_notes),
        target_language,
    )

    return translated_notes


def translate_encryption_compliance_report(
    report_text: str,
    target_language: str = DEEPL_DEFAULT_TARGET_LANG,
    api_key: Optional[str] = None,
    chunk_size: int = 5000,
) -> List[Dict[str, Any]]:
    """
    Translate an encryption or compliance report that may be large.
    Chunks the text if needed for DeepL API limits.

    Provider: DeepL API
    """
    chunks = []
    if len(report_text) <= chunk_size:
        chunks.append(report_text)
    else:
        sentences = report_text.split(". ")
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= chunk_size:
                current_chunk += (". " if current_chunk else "") + sentence
            else:
                chunks.append(current_chunk)
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk)

    results = []
    for chunk in chunks:
        result = translate_compliance_note(
            text=chunk,
            target_language=target_language,
            api_key=api_key,
        )
        results.append(result)

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Translate encryption or compliance notes for reviewers"
    )
    parser.add_argument(
        "--text",
        help="Text to translate",
    )
    parser.add_argument(
        "--text-file",
        help="Path to file containing text to translate",
    )
    parser.add_argument(
        "--notes-file",
        help="Path to JSON file with notes to batch translate",
    )
    parser.add_argument(
        "--target-lang",
        default=DEEPL_DEFAULT_TARGET_LANG,
        help="Target language code (e.g., EN-US, DE, FR)",
    )
    parser.add_argument(
        "--source-lang",
        help="Source language code (default: auto-detect)",
    )
    parser.add_argument(
        "--formality",
        choices=["default", "more", "less", "prefer_more", "prefer_less"],
        help="Formality level for translation",
    )
    parser.add_argument("--api-key", help="DeepL API key (or set DEEPL_AUTH_KEY)")
    parser.add_argument(
        "--output-file",
        help="Path to write translated output",
    )
    args = parser.parse_args()

    if args.notes_file:
        with open(args.notes_file, "r") as f:
            notes = json.load(f)

        translated = translate_compliance_notes_batch(
            notes=notes,
            target_language=args.target_lang,
            source_language=args.source_lang,
            api_key=args.api_key,
            formality=args.formality,
        )
        output = translated

    else:
        if args.text_file:
            with open(args.text_file, "r") as f:
                text = f.read()
        elif args.text:
            text = args.text
        else:
            parser.error("--text, --text-file, or --notes-file is required")

        if len(text) > 5000:
            results = translate_encryption_compliance_report(
                report_text=text,
                target_language=args.target_lang,
                api_key=args.api_key,
            )
            full_translation = " ".join(
                r["translated_text"] for r in results
            )
            output = {
                "original_text": text,
                "translated_text": full_translation,
                "target_language": args.target_lang,
                "chunks_processed": len(results),
            }
        else:
            result = translate_compliance_note(
                text=text,
                target_language=args.target_lang,
                source_language=args.source_lang,
                api_key=args.api_key,
                formality=args.formality,
            )
            output = result

    if args.output_file:
        with open(args.output_file, "w") as f:
            if isinstance(output, list):
                json.dump(output, f, indent=2, ensure_ascii=False)
            else:
                json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"Translation written to {args.output_file}")
    else:
        if isinstance(output, list):
            for note in output:
                print(
                    f"[{note.get('detected_source_language', '?')} -> {note.get('target_language', '?')}]"
                )
                print(f"  Original: {note.get('text', note.get('original_text', ''))[:80]}")
                print(f"  Translation: {note.get('translated_text', '')[:80]}")
        else:
            print(f"Detected Source: {output.get('detected_source_language', '?')}")
            print(f"Target: {output.get('target_language', '?')}")
            print(f"Translation:\n{output.get('translated_text', '')}")


if __name__ == "__main__":
    main()
