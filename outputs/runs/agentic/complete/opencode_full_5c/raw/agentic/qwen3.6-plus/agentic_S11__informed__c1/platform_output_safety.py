import os
from typing import Optional

from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models as green_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from model_models import SafetyResult

ALIBABA_GREEN_ENDPOINT = "green-cip.cn-shanghai.aliyuncs.com"


def _build_alibaba_green_client() -> Client:
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        raise RuntimeError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET "
            "environment variables are required for Alibaba Content Moderation"
        )
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=ALIBABA_GREEN_ENDPOINT,
    )
    return Client(config)


def check_platform_output_safety(
    text: str,
    service: str = "comment_detection",
    service_parameters: Optional[dict] = None,
) -> SafetyResult:
    client = _build_alibaba_green_client()

    if service_parameters is None:
        service_parameters = {}

    text_moderation_request = green_models.TextModerationRequest(
        service=service,
        service_parameters=service_parameters,
    )

    text_moderation_request.content = text

    runtime = util_models.RuntimeOptions()
    response = client.text_moderation(text_moderation_request, runtime)

    body = response.body
    code = body.code if body else None
    data = body.data if body else None

    categories = {}
    scores = {}
    is_safe = True

    if data and hasattr(data, "results") and data.results:
        for result_item in data.results:
            label = getattr(result_item, "label", "")
            rate = getattr(result_item, "rate", "")
            categories[label] = rate == "block"
            if rate == "block":
                is_safe = False

            if hasattr(result_item, "details") and result_item.details:
                for detail in result_item.details:
                    label_detail = getattr(detail, "label", "")
                    score_val = getattr(detail, "rate", 0.0)
                    if isinstance(score_val, (int, float)):
                        scores[label_detail] = float(score_val)

    return SafetyResult(
        is_safe=is_safe,
        categories=categories,
        scores=scores,
        raw_response=response,
    )


def check_text_for_harmful_content(
    text: str,
) -> SafetyResult:
    return check_platform_output_safety(
        text=text,
        service="comment_detection",
    )


def check_text_for_spam(
    text: str,
) -> SafetyResult:
    return check_platform_output_safety(
        text=text,
        service="spam_detection",
    )
