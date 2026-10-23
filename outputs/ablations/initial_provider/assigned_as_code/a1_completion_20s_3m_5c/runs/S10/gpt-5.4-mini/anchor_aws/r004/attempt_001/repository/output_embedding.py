import boto3

from model_client import get_bedrock_config
from model_models import normalize_text


def output_embedding(payload, config=None):
    cfg = get_bedrock_config(config)
    client = boto3.client("bedrock-runtime", region_name=cfg["region"])
    text = normalize_text(payload.get("text", ""))
    response = client.invoke_model(
        modelId="cohere.embed-english-v3",
        body=("{" + f'"texts":["{text.replace("\\", "\\\\").replace("\"", "\\\"")}"],"input_type":"search_document"' + "}").encode(),
        contentType="application/json",
        accept="application/json",
    )
    body = response["body"].read().decode()
    return {"text": body}
