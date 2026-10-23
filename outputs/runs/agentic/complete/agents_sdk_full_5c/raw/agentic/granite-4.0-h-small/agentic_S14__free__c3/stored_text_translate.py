'''Translate extracted text using AWS Translate.'''
import boto3
from typing import List, Tuple

def stored_text_translate(source_text: List[str], target_language_code: str = 'es') -> Tuple[str, List[str]]:
    """Translate a list of text lines from source to target language.

    Args:
        source_text: List of plain text lines extracted from a document.
        target_language_code: Language code (e.g., 'es' for Spanish). Default Spanish.

    Returns:
        Tuple of (detected_source_language, list_of_translated_lines).
    """
    translate = boto3.client('translate')
    # Infer source language (optional)
    inferred = translate.detect_dominant_language(Input={"Text": "\n".join(source_text)})
    detected_lang = inferred['Languages'][0]['LanguageCode'] if inferred['Languages'] else 'unknown'
    translated_lines = []
    for line in source_text:
        resp = translate.translate_text(
            Text=line,
            SourceLanguageCode='auto' if detected_lang=='unknown' else detected_lang,
            TargetLanguageCode=target_language_code
        )
        translated_lines.append(resp['TranslatedText'])
    return detected_lang, translated_lines
