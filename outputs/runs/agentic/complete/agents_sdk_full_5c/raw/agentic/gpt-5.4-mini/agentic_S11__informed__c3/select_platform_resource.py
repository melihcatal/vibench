from __future__ import annotations

from typing import Any, Dict

from model_client import bedrock_client, load_config



def select_platform_resource() -> Dict[str, Any]:
    config = load_config()
    client = bedrock_client()
    response = client.list_foundation_models()
    models = response.get("modelSummaries", [])
    selected = next(
        (m for m in models if config.bedrock_model_id in (m.get("modelId", ""), m.get("modelArn", ""))),
        None,
    )
    if selected is None and models:
        selected = models[0]
    return {
        "requested_model_id": config.bedrock_model_id,
        "selected_resource": selected,
        "provider": "Amazon Bedrock",
    }
