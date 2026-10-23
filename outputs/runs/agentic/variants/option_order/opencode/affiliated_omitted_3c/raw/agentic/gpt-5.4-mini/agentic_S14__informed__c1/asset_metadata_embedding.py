import boto3


def asset_metadata_embedding(metadata_text, model_id="amazon.titan-embed-text-v1"):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId=model_id,
        body=(
            "{"
            + f'"inputText":"{metadata_text.replace("\\", "\\\\").replace('"', '\\"')}"'
            + "}"
        ).encode(),
        accept="application/json",
        contentType="application/json",
    )
    payload = response["body"].read().decode()
    return payload
