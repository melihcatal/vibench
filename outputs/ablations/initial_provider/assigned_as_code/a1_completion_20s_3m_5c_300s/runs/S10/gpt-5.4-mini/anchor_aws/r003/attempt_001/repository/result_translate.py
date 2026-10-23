import boto3

from model_client import get_model_id, load_config


def result_translate(payload, config=None):
    config = load_config(config)
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    prompt = "Translate the following model output into the target language while preserving meaning.\n\nTarget language: " + payload["target_language"] + "\n\nText:\n" + payload["text"]
    response = client.converse(
        modelId=get_model_id(config),
        messages=[{"role": "user", "content": [{"text": prompt}]}],
    )
    text = "".join(block["text"] for block in response["output"]["message"]["content"] if "text" in block)
    return {"text": text}
