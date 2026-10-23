import boto3
import re

translate = boto3.client("translate", region_name="us-west-2")


def translate_markup(markup, source_lang, target_lang):
    tag_pattern = re.compile(r"<[^>]+>")
    tags = tag_pattern.findall(markup)
    translated_parts = []
    for part in re.split(tag_pattern, markup):
        if part in tags:
            translated_parts.append(part)
        else:
            translated_part = translate.translate_text(
                Text=part,
                SourceLanguageCode=source_lang,
                TargetLanguageCode=target_lang,
            )
            translated_parts.append(translated_part.translation_text)
    return "".join(translated_parts)
