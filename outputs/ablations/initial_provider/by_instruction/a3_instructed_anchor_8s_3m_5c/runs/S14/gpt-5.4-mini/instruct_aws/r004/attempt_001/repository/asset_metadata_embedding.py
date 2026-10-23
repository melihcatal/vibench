import boto3


def embed_asset_metadata_and_text(text, dimensions=1024, model_id="amazon.titan-embed-text-v2:0"):
    bedrock = boto3.client("bedrock-runtime")
    body = {"inputText": text, "dimensions": dimensions}
    return bedrock.invoke_model(modelId=model_id, body=bytes(str(body), "utf-8"))
