import boto3

from model_client import get_model_id, load_config


def spoken_brief(payload, config=None):
    config = load_config(config)
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = "Rewrite the following model output as a short spoken brief for audio narration.\n\n" + payload["text"]
    response = client.converse(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}
