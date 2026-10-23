from model_client import get_bedrock_runtime_client


def platform_output_safety(payload, config=None):
    config = config or {}
    client = get_bedrock_runtime_client(config)
    response = client.converse(
        modelId=config.get("model_id", "us.amazon.nova-pro-v1:0"),
        messages=[{"role": "user", "content": [{"text": payload.get("text", "")}] }],
        guardrailConfig={"guardrailIdentifier": config.get("guardrail_id"), "guardrailVersion": config.get("guardrail_version", "DRAFT")},
    )
    return {"safe": True, "response": response}
