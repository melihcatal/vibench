# [LATER-STEP] invoice_note_translate.py

# Translates extracted invoice description/note fields using AWS Translate
import os
import boto3


def translate_invoice_note(note: str, target_lang: str = "es") -> str:
    """Translate the invoice note/description to the target language."""
    translate = boto3.client("translate")
    response = translate.translate_text(
        Text=note, SourceLanguageCode="en", TargetLanguageCode=target_lang
    )
    return response.TranslatedText
