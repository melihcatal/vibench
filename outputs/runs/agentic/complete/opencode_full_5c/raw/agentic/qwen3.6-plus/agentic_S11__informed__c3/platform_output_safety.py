import os
from typing import Optional

from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models
from alibabacloud_tea_openapi.models import Config

from model_models import SafetyResult


def _build_green_client() -> Client:
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET must be set"
        )
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="green-cip.cn-shanghai.aliyuncs.com",
    )
    return Client(config)


def check_platform_output_safety(
    text: str,
    scenes: Optional[list[str]] = None,
) -> SafetyResult:
    client = _build_green_client()

    if scenes is None:
        scenes = ["porn", "terrorism", "contraband", "ad", "abuse", "spam"]

    service_parameters = {
        "content": text,
        "dataId": "platform-safety-check-001",
    }

    text_moderation_request = models.TextModerationRequest(
        service="ai_art_detection",
        service_parameters=service_parameters,
    )

    try:
        response = client.text_moderation(text_moderation_request)
        result_data = response.body.data if response.body else {}
        result_list = (
            result_data.get("results", []) if isinstance(result_data, dict) else []
        )

        categories = {}
        flagged = []
        is_safe = True

        for result_item in result_list:
            label = result_item.get("label", "")
            score = float(result_item.get("rate", 0))
            categories[label] = score
            if score > 0.5:
                is_safe = False
                flagged.append(label)

        if not result_list and hasattr(response.body, "suggestion"):
            suggestion = response.body.suggestion
            if suggestion == "block":
                is_safe = False

        return SafetyResult(
            text=text,
            is_safe=is_safe,
            categories=categories,
            flagged_categories=flagged,
            raw_response=response,
            provider="Alibaba Content Moderation",
        )
    except Exception:
        return SafetyResult(
            text=text,
            is_safe=True,
            provider="Alibaba Content Moderation",
        )


if __name__ == "__main__":
    result = check_platform_output_safety("This is a safe test message.")
    print("Is safe:", result.is_safe)
    print("Provider:", result.provider)
