from speech_client import load_config
from speech_models import normalize_text_payload

import boto3


def script_translate(payload, config=None):
    cfg = load_config(config)
    client = boto3.client("translate", region_name=cfg["region"])
    text = normalize_text_payload(payload)["text"]
    response = client.translate_text(Text=text, SourceLanguageCode=payload["source_language"], TargetLanguageCode=payload["target_language"])
    return {"translated_text": response["TranslatedText"], "source_language": payload["source_language"], "target_language": payload["target_language"]}
