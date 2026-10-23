import json

from storage_client import get_bedrock_client


def asset_metadata_embedding(metadata: dict, text: str):
    bedrock = get_bedrock_client()
    payload = json.dumps(
        {"inputText": json.dumps({"metadata": metadata, "text": text}, sort_keys=True)}
    )
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=payload,
        accept="application/json",
        contentType="application/json",
    )
    return {
        "embedding": json.loads(response["body"].read().decode("utf-8")).get(
            "embedding"
        )
    }
