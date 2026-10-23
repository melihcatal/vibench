import boto3


def prompt_safety(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.apply_guardrail(
        guardrailIdentifier=config.get("guardrail_id"),
        guardrailVersion=config.get("guardrail_version", "DRAFT"),
        source="INPUT",
        content=[{"text": {"text": payload["text"]}}],
    )
    return {"safe": response.get("action", "NONE") == "NONE", "response": response}
