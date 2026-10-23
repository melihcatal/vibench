import re

import boto3

from translation_models import normalize_markup_payload


TAG_RE = re.compile(r"(<[^>]+>)")


def translate_markup(payload, config=None):
    request = normalize_markup_payload(payload)
    client = boto3.client("translate", region_name=(config or {}).get("region"))
    parts = TAG_RE.split(request["markup"])
    translated_parts = []
    for part in parts:
        if not part or TAG_RE.fullmatch(part):
            translated_parts.append(part)
            continue
        response = client.translate_text(
            Text=part,
            SourceLanguageCode=request["source_language"],
            TargetLanguageCode=request["target_language"],
        )
        translated_parts.append(response["TranslatedText"])
    return {
        "markup": "".join(translated_parts),
        "source_language": request["source_language"],
        "target_language": request["target_language"],
    }
