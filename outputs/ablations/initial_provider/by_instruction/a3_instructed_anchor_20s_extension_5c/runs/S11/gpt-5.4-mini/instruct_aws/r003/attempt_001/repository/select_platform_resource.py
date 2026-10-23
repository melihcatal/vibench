from model_client import load_bedrock_client, model_id_for_request


def select_platform_resource(model_id: str = None):
    client = load_bedrock_client()
    resolved_model_id = model_id or model_id_for_request()
    response = client.get_foundation_model(modelIdentifier=resolved_model_id)
    return {
        "model_id": resolved_model_id,
        "resource_id": response.get("modelDetails", {}).get("modelArn", resolved_model_id),
        "raw": response,
    }
