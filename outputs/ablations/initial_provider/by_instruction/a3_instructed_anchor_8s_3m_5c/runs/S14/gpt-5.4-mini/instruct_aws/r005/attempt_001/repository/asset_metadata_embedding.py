import boto3

from storage_models import normalize_text


def asset_metadata_embedding(metadata, extracted_text, model_id: str = "amazon.titan-embed-text-v2:0"):
    bedrock = boto3.client("bedrock-runtime")
    payload = normalize_text(metadata) + "\n" + normalize_text(extracted_text)
    response = bedrock.invoke_model(
        modelId=model_id,
        body=("{" + f'"inputText":"{payload.replace("\\", "\\\\").replace("\"", "\\\"")}"' + "}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    body = response["body"].read().decode("utf-8")
    return body
