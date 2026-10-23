from typing import Dict, Optional

from model_client import bedrock_service_client, load_config


def select_platform_resource(
    preferred_model_id: Optional[str] = None,
) -> Dict[str, str]:
    config = load_config()
    model_id = preferred_model_id or config["model_id"]
    inference_profile_id = config.get("inference_profile_id")
    client = bedrock_service_client(config["region"])
    if inference_profile_id:
        return {
            "resource_type": "inference-profile",
            "resource_id": inference_profile_id,
            "model_id": model_id,
        }
    try:
        client.get_foundation_model(modelIdentifier=model_id)
    except Exception:
        pass
    return {
        "resource_type": "foundation-model",
        "resource_id": model_id,
        "model_id": model_id,
    }
