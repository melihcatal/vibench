import os
import sys
import json

from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models
from alibabacloud_tea_openapi.models import Config

from observability_models import IncidentFinding


def create_green_client() -> Client:
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="green-cip.cn-shanghai.aliyuncs.com",
        connect_timeout=10000,
        read_timeout=3000,
    )
    return Client(config)


def check_log_text_safety(text: str, service: str = "comment_detection") -> dict:
    client = create_green_client()

    text_moderation_request = models.TextModerationPlusRequest(
        service=service,
        content=text,
    )

    try:
        response = client.text_moderation_plus(text_moderation_request)
        result = {
            "text": text,
            "safe": True,
            "labels": [],
            "suggestion": "pass",
            "raw_response": None,
        }

        if response.body and response.body.code == 200:
            data = response.body.data
            if data:
                result["suggestion"] = (
                    data.suggestion if hasattr(data, "suggestion") else "pass"
                )
                result["safe"] = (
                    data.suggestion == "pass" if hasattr(data, "suggestion") else True
                )
                if hasattr(data, "results") and data.results:
                    for item in data.results:
                        if hasattr(item, "label"):
                            result["labels"].append(item.label)
                if hasattr(data, "label"):
                    result["labels"].append(data.label)
        else:
            result["error"] = (
                f"API returned code: {response.body.code if response.body else 'unknown'}"
            )

        return result
    except Exception as e:
        return {
            "text": text,
            "safe": True,
            "labels": [],
            "suggestion": "pass",
            "error": str(e),
        }


def check_multiple_log_texts(texts: list[str]) -> list[dict]:
    results = []
    for text in texts:
        safety_result = check_log_text_safety(text)
        results.append(safety_result)
    return results


def annotate_findings_with_safety(
    findings: list[IncidentFinding],
) -> list[IncidentFinding]:
    annotated = []
    for finding in findings:
        message = finding.log_entry.get("message", "")
        if message:
            safety_result = check_log_text_safety(message)
            finding.safety_flags = safety_result.get("labels", [])
            if not safety_result.get("safe", True):
                finding.safety_flags.append("unsafe_content")
        annotated.append(finding)
    return annotated


if __name__ == "__main__":
    text = (
        sys.argv[1] if len(sys.argv) > 1 else "Sample log message to check for safety"
    )
    result = check_log_text_safety(text)
    print(json.dumps(result, indent=2))
