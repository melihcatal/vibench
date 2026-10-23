"""
Translate text extracted from a stored document using DeepL API.

Uses deepl SDK for DeepL Translation (service=DeepL API).
Environment variable: DEEPL_AUTH_KEY
"""

from typing import List, Optional

import deepl

from stored_document_ocr import run_ocr_on_stored_document, _extract_text_from_blocks


def _get_deepl_translator() -> deepl.Translator:
    """
    Create a DeepL translator client using the DEEPL_AUTH_KEY environment variable.

    Returns:
        deepl.Translator: Authenticated DeepL client.

    Raises:
        ValueError: If DEEPL_AUTH_KEY is not set.
    """
    auth_key = __import__("os").environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError(
            "DEEPL_AUTH_KEY environment variable must be set for DeepL translation"
        )
    return deepl.Translator(auth_key)


def translate_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    split_sentences: Optional[str] = None,
) -> str:
    """
    Translate a text string using the DeepL API.

    Args:
        text: The text to translate.
        target_lang: Target language code (e.g., "DE", "FR", "JA", "ZH").
        source_lang: Optional source language code; DeepL auto-detects if not provided.
        formality: Optional formality level ("more" or "less").
        split_sentences: Sentence splitting mode ("on", "off", "nonewlines").

    Returns:
        str: The translated text.

    Raises:
        deepl.DeepLException: On API errors.
    """
    translator = _get_deepl_translator()

    kwargs = {
        "target_lang": target_lang.upper(),
    }

    if source_lang:
        kwargs["source_lang"] = source_lang.upper()
    if formality:
        kwargs["formality"] = formality
    if split_sentences:
        kwargs["split_sentences"] = split_sentences

    result = translator.translate_text(text, **kwargs)
    return result.text


def translate_stored_document(
    bucket: str,
    object_key: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    prefix: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
) -> dict:
    """
    Run OCR on a stored S3 document and translate the extracted text using DeepL.

    Args:
        bucket: The S3 bucket containing the document.
        object_key: The S3 object key of the document.
        target_lang: Target language code (e.g., "DE", "FR", "JA").
        source_lang: Optional source language code for auto-detection.
        prefix: Optional prefix for the S3 object key.
        formality: Optional formality level for translation.
        preserve_formatting: If True, translate line-by-line to preserve structure.

    Returns:
        dict with keys:
            - original_text: The OCR-extracted text
            - translated_text: The full translated text
            - target_lang: The target language code
            - source_lang: Detected or specified source language
            - lines: List of per-line translations (if preserve_formatting is True)
    """
    ocr_result = run_ocr_on_stored_document(bucket, object_key, prefix=prefix)
    original_text = ocr_result["text"]

    if not original_text.strip():
        return {
            "original_text": "",
            "translated_text": "",
            "target_lang": target_lang,
            "source_lang": source_lang,
            "lines": [],
        }

    if preserve_formatting:
        lines = original_text.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]

        translated_lines_map = {}
        for i, line in enumerate(non_empty_lines):
            try:
                translated_line = translate_text(
                    text=line,
                    target_lang=target_lang,
                    source_lang=source_lang,
                    formality=formality,
                )
                translated_lines_map[line] = translated_line
            except Exception:
                translated_lines_map[line] = line

        translated_lines = []
        for line in lines:
            if line.strip() and line in translated_lines_map:
                translated_lines.append(translated_lines_map[line])
            else:
                translated_lines.append(line)

        translated_text = "\n".join(translated_lines)
        line_details = translated_lines
    else:
        translated_text = translate_text(
            text=original_text,
            target_lang=target_lang,
            source_lang=source_lang,
            formality=formality,
        )
        line_details = translated_text.split("\n")

    return {
        "original_text": original_text,
        "translated_text": translated_text,
        "target_lang": target_lang.upper(),
        "source_lang": source_lang.upper() if source_lang else "auto",
        "lines": line_details,
    }


def translate_batch(
    texts: List[str],
    target_lang: str,
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> List[str]:
    """
    Translate a batch of text strings using the DeepL API in a single call.

    Args:
        texts: List of text strings to translate.
        target_lang: Target language code.
        source_lang: Optional source language code.
        formality: Optional formality level.

    Returns:
        List[str]: List of translated texts in the same order.
    """
    if not texts:
        return []

    translator = _get_deepl_translator()

    kwargs = {
        "target_lang": target_lang.upper(),
    }
    if source_lang:
        kwargs["source_lang"] = source_lang.upper()
    if formality:
        kwargs["formality"] = formality

    results = translator.translate_text(texts, **kwargs)

    if isinstance(results, list):
        return [r.text for r in results]
    return [results.text]
