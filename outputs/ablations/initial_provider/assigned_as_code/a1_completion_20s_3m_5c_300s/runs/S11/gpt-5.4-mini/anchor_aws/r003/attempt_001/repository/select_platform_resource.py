import boto3


def select_platform_resource(config=None):
    config = config or {}
    client = boto3.client("bedrock", region_name=config.get("region", "us-east-1"))
    model_ids = config.get("model_ids", ["us.amazon.nova-pro-v1:0"])
    response = client.list_foundation_models() if hasattr(client, "list_foundation_models") else {"modelSummaries": []}
    summaries = response.get("modelSummaries", [])
    preferred = config.get("preferred_model_id")
    if preferred:
        return {"modelId": preferred}
    for summary in summaries:
        model_id = summary.get("modelId")
        if model_id in model_ids:
            return {"modelId": model_id}
    return {"modelId": model_ids[0]}
