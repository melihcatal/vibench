import os
from typing import Optional

from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models
from alibabacloud_tea_openapi.models import Config

from model_models import SafetyResult


ALIBABA_CLOUD_ACCESS_KEY_ID_ENV = "ALIBABA_CLOUD_ACCESS_KEY_ID"
ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV = "ALIBABA_CLOUD_ACCESS_KEY_SECRET"


def _create_green_client() -> Client:
    access_key_id = os.environ.get(ALIBABA_CLOUD_ACCESS_KEY_ID_ENV)
    access_key_secret = os.environ.get(ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV)
    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are required for Alibaba Content Moderation"
        )
    config = Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="green-cip.cn-shanghai.aliyuncs.com",
        connect_timeout=10000,
        read_timeout=30000,
    )
    return Client(config)


def check_platform_output_safety(
    text: str,
    scenes: Optional[list] = None,
) -> SafetyResult:
    client = _create_green_client()

    if scenes is None:
        scenes = ["antispam"]

    text_moderation_request = models.TextModerationPlusRequest(
        service="comment_detection",
        service_parameters={
            "content": text,
            "dataId": "platform_safety_check",
        },
    )

    try:
        runtime = models.RuntimeOptions()
        response = client.text_moderation_plus_with_options(
            text_moderation_request, runtime
        )

        body = response.body
        result_data = body.data if body and hasattr(body, "data") else None

        is_safe = True
        categories = {}
        risk_level = "pass"

        if result_data and hasattr(result_data, "result"):
            for item in result_data.result:
                label = item.label if hasattr(item, "label") else ""
                rate = item.rate if hasattr(item, "rate") else 0.0

                if label:
                    categories[label] = rate
                    if rate >= 0.5:
                        is_safe = False
                        risk_level = "block" if rate >= 0.9 else "review"

        return SafetyResult(
            text=text,
            is_safe=is_safe,
            categories=categories,
            risk_level=risk_level,
            raw_response=response,
        )

    except Exception as e:
        return SafetyResult(
            text=text,
            is_safe=False,
            categories={"error": str(e)},
            risk_level="error",
        )
