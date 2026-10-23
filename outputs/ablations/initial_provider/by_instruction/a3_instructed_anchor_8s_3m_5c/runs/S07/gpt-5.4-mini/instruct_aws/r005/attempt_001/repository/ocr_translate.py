import json
from typing import Any, Dict

import boto3


def translate_ocr_text(payload: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("translate")
    text = payload.get("text", "")
    target_language = payload.get("target_language", "en")
    response = client.translate_text(Text=text, SourceLanguageCode=payload.get("source_language", "auto"), TargetLanguageCode=target_language)
    return {"translated_text": response.get("TranslatedText", ""), "source_language": response.get("SourceLanguageCode", payload.get("source_language", "auto")), "target_language": response.get("TargetLanguageCode", target_language), "raw": response}


if __name__ == "__main__":
    import sys

    print(json.dumps(translate_ocr_text(json.loads(sys.stdin.read())), ensure_ascii=False))
