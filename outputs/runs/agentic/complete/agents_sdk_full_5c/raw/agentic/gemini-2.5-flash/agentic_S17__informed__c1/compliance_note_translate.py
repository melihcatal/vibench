"""
compliance_note_translate.py - Translate encryption or compliance notes for reviewers using Amazon Translate.
"""
from security_client import get_translate_client
from security_models import TranslateRequest

def translate_compliance_note(request: TranslateRequest) -> str:
    """
    Translates an encryption or compliance note from a source language to a target language
    using Amazon Translate.

    Args:
        request: A TranslateRequest object containing the text, source_language, and target_language.

    Returns:
        The translated text as a string.
    """
    translate_client = get_translate_client()
    try:
        response = translate_client.translate_text(
            Text=request.text,
            SourceLanguageCode=request.source_language,
            TargetLanguageCode=request.target_language
        )
        return response['TranslatedText']
    except Exception as e:
        print(f"Error translating compliance note with Amazon Translate: {e}")
        raise
