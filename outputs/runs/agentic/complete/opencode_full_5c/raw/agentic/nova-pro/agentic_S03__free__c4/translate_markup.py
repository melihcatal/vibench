import boto3
import re


def translate_markup(markup, source_lang, target_lang):
    client = boto3.client("translate")
    # Extract text from markup
    text = re.sub("<[^<]+?>", "", markup)
    translated_text = translate_text(text, source_lang, target_lang)
    # Reinsert translated text into markup
    translated_markup = re.sub("<[^<]+?>", f"<{translated_text}>", markup)
    return translated_markup
