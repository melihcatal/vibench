import os
import sys
import json

from alibabacloud_alimt20181012.client import Client
from alibabacloud_alimt20181012 import models
from alibabacloud_tea_openapi.models import Config

from observability_models import IncidentFinding


def create_translator_client() -> Client:
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="mt.cn-hangzhou.aliyuncs.com",
    )
    return Client(config)


def translate_log_message(
    text: str,
    source_language: str = "zh",
    target_language: str = "en",
    scene: str = "general",
) -> dict:
    client = create_translator_client()

    request = models.TranslateGeneralRequest(
        format_type="text",
        source_language=source_language,
        target_language=target_language,
        source_text=text,
        scene=scene,
    )

    try:
        response = client.translate_general(request)
        result = {
            "original_text": text,
            "translated_text": "",
            "source_language": source_language,
            "target_language": target_language,
        }

        if response.body and response.body.code == 200:
            data = response.body.data
            if data and hasattr(data, "translated"):
                result["translated_text"] = data.translated
        else:
            result["error"] = (
                f"Translation API returned code: {response.body.code if response.body else 'unknown'}"
            )

        return result
    except Exception as e:
        return {
            "original_text": text,
            "translated_text": text,
            "source_language": source_language,
            "target_language": target_language,
            "error": str(e),
        }


def translate_multiple_log_messages(
    texts: list[str],
    source_language: str = "zh",
    target_language: str = "en",
) -> list[dict]:
    results = []
    for text in texts:
        translation_result = translate_log_message(
            text=text,
            source_language=source_language,
            target_language=target_language,
        )
        results.append(translation_result)
    return results


def annotate_findings_with_translation(
    findings: list[IncidentFinding],
    source_language: str = "zh",
    target_language: str = "en",
) -> list[IncidentFinding]:
    annotated = []
    for finding in findings:
        message = finding.log_entry.get("message", "")
        if message:
            translation_result = translate_log_message(
                text=message,
                source_language=source_language,
                target_language=target_language,
            )
            finding.translated_message = translation_result.get("translated_text", "")
        annotated.append(finding)
    return annotated


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Sample log message to translate"
    target = sys.argv[2] if len(sys.argv) > 2 else "en"
    source = sys.argv[3] if len(sys.argv) > 3 else "zh"
    result = translate_log_message(
        text=text, source_language=source, target_language=target
    )
    print(json.dumps(result, indent=2))
