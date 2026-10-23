from __future__ import annotations

from typing import Optional

from model_client import (
    DEFAULT_MODEL_ID,
    get_bedrock_control_client,
    load_platform_resource,
)
from model_models import PlatformResource


def select_platform_resource(
    preferred_model_id: Optional[str] = None,
) -> PlatformResource:
    resource = load_platform_resource()
    control_client = get_bedrock_control_client(resource.region_name)
    model_id = preferred_model_id or resource.model_id or DEFAULT_MODEL_ID
    model_summary = control_client.get_foundation_model(modelIdentifier=model_id)
    details = model_summary.get("modelDetails", {})
    resolved_model_id = details.get("modelId", model_id)
    return PlatformResource(
        inference_profile_arn=resource.inference_profile_arn,
        region_name=resource.region_name,
        model_id=resolved_model_id,
    )
