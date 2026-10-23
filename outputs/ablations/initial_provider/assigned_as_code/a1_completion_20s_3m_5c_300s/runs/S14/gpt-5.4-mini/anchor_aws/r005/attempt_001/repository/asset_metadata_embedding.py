import boto3

from storage_models import normalize_object_name


def asset_metadata_embedding(payload, config=None):
    config = dict(config or {})
    s3 = boto3.client("s3", region_name=config.get("region"))
    bedrock = boto3.client("bedrock-runtime", region_name=config.get("region"))
    head = s3.head_object(Bucket=config["bucket"], Key=normalize_object_name(payload["object_name"]))
    text = payload.get("text", "")
    source = f'{head.get("ContentType", "")} {head.get("Metadata", {})} {text}'
    response = bedrock.invoke_model(
        modelId=config.get("embedding_model_id", "amazon.titan-embed-text-v2:0"),
        body=("{" + f'"inputText":"{source.replace("\\", "\\\\").replace("\"", "\\\"")}"' + "}").encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    return {"vector": response["body"].read().decode("utf-8")}
