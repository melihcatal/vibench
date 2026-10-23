from __future__ import annotations

from typing import Any, Dict

from model_client import bedrock_client, load_platform_config


BEDROCK_CATALOG_MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def select_platform_resource(model_id: str = BEDROCK_CATALOG_MODEL_ID) -> Dict[str, Any]:
    config = load_platform_config()
    client = bedrock_client(config["aws_region"])
    response = client.list_foundation_models(byProvider="anthropic")
    models = response.get("modelSummaries", [])
    selected = next((item for item in models if item.get("modelId") == model_id), None)
    return {
        "selected": selected or {"modelId": model_id, "modelArn": f"arn:aws:bedrock:{config['aws_region']}::foundation-model/{model_id}"},
        "catalog": response,
    }
