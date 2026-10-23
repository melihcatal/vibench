import boto3
import json
import os


def asset_metadata_embedding(payload, config=None):
    config = config or {}
    bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=config.get("region") or os.environ.get("AWS_REGION"))
    extracted_text = payload.get("extracted_text", "")
    metadata = payload.get("metadata", {})

    # Combine text and metadata for embedding
    combined_text = extracted_text
    if metadata:
        for key, value in metadata.items():
            combined_text += f" {key}: {value}"

    # Using Amazon Titan Embeddings model
    model_id = "amazon.titan-embed-text-v1"

    body = json.dumps({"inputText": combined_text})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding", [])

    return {"input_text": combined_text, "embedding": embedding}
