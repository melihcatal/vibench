from __future__ import annotations

from typing import Optional

from model_client import default_resource_selection, get_bedrock_control_client
from model_models import ResourceSelection


def select_platform_resource(
    model_id: Optional[str] = None, region_name: Optional[str] = None
) -> ResourceSelection:
    selection = default_resource_selection()
    if model_id:
        selection.model_id = model_id
    if region_name:
        selection.region_name = region_name
    control_client = get_bedrock_control_client(selection.region_name)
    if selection.inference_profile_arn:
        response = control_client.get_inference_profile(
            inferenceProfileIdentifier=selection.inference_profile_arn
        )
        profile = response.get("inferenceProfileArn", selection.inference_profile_arn)
        models = response.get("models", [])
        if models:
            selection.model_id = models[0].get("modelArn", selection.model_id)
        selection.inference_profile_arn = profile
    return selection
