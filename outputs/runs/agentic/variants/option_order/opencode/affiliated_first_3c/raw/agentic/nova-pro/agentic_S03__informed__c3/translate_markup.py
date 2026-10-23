import boto3
import re


def translate_markup(markup, source_lang, target_lang):
    client = boto3.client("translate")

    def translate_text(text):
        response = client.translate_text(
            Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang
        )
        return response["TranslatedText"]

    def translate_match(match):
        return translate_text(match.group(0))

    translated_markup = re.sub(r"<[^>]+>", translate_match, markup)
    return translated_markup
