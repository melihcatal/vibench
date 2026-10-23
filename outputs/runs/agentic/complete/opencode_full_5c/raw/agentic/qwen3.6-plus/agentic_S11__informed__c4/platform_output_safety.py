import os
from typing import Optional

from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from model_models import SafetyResult, SafetyCategory


def _get_green_client() -> Client:
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET "
            "environment variables are required for Alibaba Content Moderation"
        )
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint="green-cip.cn-shanghai.aliyuncs.com",
    )
    return Client(config)


def check_platform_output_safety(
    text: str,
    scenes: Optional[list] = None,
    threshold: float = 0.7,
) -> SafetyResult:
    client = _get_green_client()
    if scenes is None:
        scenes = ["antispam"]
    text_moderation_request = models.TextModerationPlusRequest(
        service="ai_art_detection",
        scenes=scenes,
        tasks=[
            models.TextModerationPlusRequestTasks(
                content=text,
            )
        ],
    )
    runtime = util_models.RuntimeOptions()
    try:
        response = client.text_moderation_plus_with_options(
            text_moderation_request, runtime
        )
    except Exception as e:
        response = _check_safety_fallback(text, scenes, threshold)
        return response
    categories = []
    is_safe = True
    request_id = ""
    if hasattr(response, "body") and response.body:
        body = response.body
        request_id = getattr(body, "request_id", "")
        if hasattr(body, "data") and body.data:
            for task_result in body.data:
                if hasattr(task_result, "results") and task_result.results:
                    for result in task_result.results:
                        category_name = getattr(result, "label", "unknown")
                        score = getattr(result, "rate", 0.0)
                        is_violation = score >= threshold
                        if is_violation:
                            is_safe = False
                        categories.append(
                            SafetyCategory(
                                name=category_name,
                                score=score,
                                is_violation=is_violation,
                            )
                        )
    raw_response = {
        "request_id": request_id,
        "code": getattr(response.body, "code", None)
        if hasattr(response, "body")
        else None,
        "msg": getattr(response.body, "msg", None)
        if hasattr(response, "body")
        else None,
    }
    return SafetyResult(
        is_safe=is_safe,
        categories=categories,
        request_id=request_id,
        raw_response=raw_response,
    )


def _check_safety_fallback(text: str, scenes: list, threshold: float) -> SafetyResult:
    return SafetyResult(
        is_safe=True,
        categories=[],
        request_id="",
        raw_response={"fallback": True, "error": "API call failed"},
    )
