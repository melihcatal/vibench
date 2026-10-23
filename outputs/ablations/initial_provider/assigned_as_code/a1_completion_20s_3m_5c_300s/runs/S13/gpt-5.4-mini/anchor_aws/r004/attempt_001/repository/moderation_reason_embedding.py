from safety_client import load_safety_config


def moderation_reason_embedding(payload, config=None):
    import boto3

    cfg = load_safety_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    text = (payload or {}).get("text", "")
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=("{" + f'"inputText":"{text}"' + "}").encode("utf-8"), contentType="application/json", accept="application/json")
    return {"embedding_response": response.get("body").read().decode("utf-8"), "provider": "amazon.titan-embed-text-v2:0"}
