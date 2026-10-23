import boto3
from storage_client import get_storage_config, get_s3_client
from storage_models import normalize_key


def asset_metadata_embedding(payload, config=None):
    config = get_storage_config(config)
    s3 = get_s3_client(config)
    obj = s3.get_object(Bucket=config["bucket"], Key=normalize_key(payload))
    text = obj["Body"].read().decode("utf-8")
    metadata = s3.head_object(Bucket=config["bucket"], Key=normalize_key(payload))
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=("{" + f'"inputText":"{metadata.get("ContentType", "")}"' + "}").encode("utf-8"))
    return {"object_name": normalize_key(payload), "text": text, "metadata": metadata, "embedding_response": response}
