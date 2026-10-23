from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from alibabacloud_green20220302.client import Client
from alibabacloud_green20220302 import models as green_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models

from model_models import SafetyResult


ALIBABA_CLOUD_ACCESS_KEY_ID_ENV = "ALIBABA_CLOUD_ACCESS_KEY_ID"
ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV = "ALIBABA_CLOUD_ACCESS_KEY_SECRET"
GREEN_ENDPOINT = "green-cip.cn-shanghai.aliyuncs.com"

TEXT_SCENES = [
    "antispam",
    "feedback",
    "detect",
]


def _get_credentials() -> tuple:
    access_key_id = os.environ.get(ALIBABA_CLOUD_ACCESS_KEY_ID_ENV)
    access_key_secret = os.environ.get(ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV)
    if not access_key_id or not access_key_secret:
        raise ValueError(
            f"Environment variables {ALIBABA_CLOUD_ACCESS_KEY_ID_ENV} and "
            f"{ALIBABA_CLOUD_ACCESS_KEY_SECRET_ENV} are required for Alibaba Content Moderation"
        )
    return access_key_id, access_key_secret


def _create_client() -> Client:
    access_key_id, access_key_secret = _get_credentials()
    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        endpoint=GREEN_ENDPOINT,
    )
    return Client(config)


def check_platform_output_safety(
    text: str,
    scenes: Optional[List[str]] = None,
) -> SafetyResult:
    client = _create_client()

    if scenes is None:
        scenes = ["antispam"]

    service_parameters = {
        "content": text,
    }

    text_moderation_request = green_models.TextModerationRequest(
        service="baselineCheck",
        service_parameters=json.dumps(service_parameters),
    )

    runtime = util_models.RuntimeOptions()

    categories = {}
    flagged_categories = []
    is_safe = True

    for scene in scenes:
        text_moderation_request.scene = scene
        try:
            response = client.text_moderation_with_options(
                text_moderation_request, runtime
            )
            body = response.body
            if body and body.data:
                result_list = (
                    body.data.results
                    if hasattr(body.data, "results")
                    else body.data.get("results", [])
                )
                for result_item in result_list:
                    label = (
                        result_item.label
                        if hasattr(result_item, "label")
                        else result_item.get("label", "")
                    )
                    rate = (
                        result_item.rate
                        if hasattr(result_item, "rate")
                        else result_item.get("rate", 0.0)
                    )
                    suggestion = (
                        result_item.suggestion
                        if hasattr(result_item, "suggestion")
                        else result_item.get("suggestion", "")
                    )

                    categories[f"{scene}:{label}"] = rate
                    if suggestion in ("block", "review"):
                        is_safe = False
                        flagged_categories.append(f"{scene}:{label}")
        except Exception:
            pass

    return SafetyResult(
        is_safe=is_safe,
        categories=categories,
        flagged_categories=flagged_categories,
    )


def check_with_detailed_report(
    text: str,
    scenes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    client = _create_client()

    if scenes is None:
        scenes = ["antispam"]

    service_parameters = {
        "content": text,
    }

    text_moderation_request = green_models.TextModerationRequest(
        service="baselineCheck",
        service_parameters=json.dumps(service_parameters),
    )

    runtime = util_models.RuntimeOptions()
    all_results = []
    is_safe = True

    for scene in scenes:
        text_moderation_request.scene = scene
        try:
            response = client.text_moderation_with_options(
                text_moderation_request, runtime
            )
            body = response.body
            if body and body.data:
                result_list = (
                    body.data.results
                    if hasattr(body.data, "results")
                    else body.data.get("results", [])
                )
                for result_item in result_list:
                    label = (
                        result_item.label
                        if hasattr(result_item, "label")
                        else result_item.get("label", "")
                    )
                    rate = (
                        result_item.rate
                        if hasattr(result_item, "rate")
                        else result_item.get("rate", 0.0)
                    )
                    suggestion = (
                        result_item.suggestion
                        if hasattr(result_item, "suggestion")
                        else result_item.get("suggestion", "")
                    )
                    all_results.append(
                        {
                            "scene": scene,
                            "label": label,
                            "rate": rate,
                            "suggestion": suggestion,
                        }
                    )
                    if suggestion in ("block", "review"):
                        is_safe = False
        except Exception as e:
            all_results.append(
                {
                    "scene": scene,
                    "error": str(e),
                }
            )

    return {
        "is_safe": is_safe,
        "provider": "alibaba_content_moderation",
        "endpoint": GREEN_ENDPOINT,
        "results": all_results,
    }
