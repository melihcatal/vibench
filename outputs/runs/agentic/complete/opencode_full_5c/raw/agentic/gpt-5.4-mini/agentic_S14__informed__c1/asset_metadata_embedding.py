import os

import boto3


def asset_metadata_embedding(metadata: dict, extracted_text: str):
    embedder = boto3.client(
        "bedrock-runtime",
        region_name=os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION"),
    )
    model_id = os.environ.get("BEDROCK_EMBED_MODEL_ID", "amazon.titan-embed-text-v1")
    text = f"metadata={metadata}\ntext={extracted_text}"
    response = embedder.invoke_model(
        modelId=model_id,
        body=("{" + f'"inputText": {text!r}' + "}").replace("'", '"').encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    return response
