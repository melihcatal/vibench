import boto3

from model_client import load_config


def output_embedding(payload, config=None):
    config = load_config(config)
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=("{" + f'"inputText":"{payload["text"]}"' + "}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    body = response["body"].read().decode("utf-8")
    return {"embedding": body}
