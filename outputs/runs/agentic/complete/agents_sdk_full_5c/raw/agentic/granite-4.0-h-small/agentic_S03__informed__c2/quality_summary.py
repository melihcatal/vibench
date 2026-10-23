import os
from typing import List, Dict
from translation_client import TranslationClient
from translation_models import TranslationModels

def summarize_quality(translations: List[Dict[str, str]], source_texts: List[str]) -> Dict[str, List[str]]:
    """Identify and summarize potential translation quality issues.

    This simplistic implementation flags missing translations, non‑ASCII characters
    when a Latin target is expected, and empty strings.

    Args:
        translations: List of translation response dicts (each must have 'translatedText').
        source_texts:  Original source strings, aligned by index.
    Returns:
        Dict with issue categories as keys and lists of problematic source texts as values.
    """
    issues: Dict[str, List[str]] = {
        "missing_translation": [],
        "empty_translation": [],
        "unexpected_non_latin": [],
    }
    client = TranslationClient()
    # Detect source language for each text
    src_langs = [client.detect_language(txt) for txt in source_texts]
    for src, target, src_lang in zip(source_texts, translations, src_langs):
        tr_text = target.get('translatedText', '')
        if not tr_text:
            issues["missing_translation"].append(src)
            continue
        if not tr_text.strip():
            issues["empty_translation"].append(src)
            continue
        # If target language is a Latin script language, flag unexpected non‑Latin chars
        if src_lang not in {'zh', 'ja', 'ko', 'ru', 'ar', 'he'}:
            if any(ord(c) > 127 for c in tr_text):
                issues["unexpected_non_latin"].append(src)
    return issues

# Demo / simple test (remove in library usage)
if __name__ == "__main__":
    client = TranslationClient()
    srcs = ["Hello", "Bonjour", "ٰاها"]  # hello in Arabic
    trans = [client.translate(txt, "fr") for txt in srcs]
    result = summarize_quality(trans, srcs)
    print(result)
