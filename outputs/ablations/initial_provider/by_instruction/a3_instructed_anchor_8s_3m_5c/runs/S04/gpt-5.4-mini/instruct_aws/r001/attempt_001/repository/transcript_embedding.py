import json

from speech_client import get_bedrock_client


def transcript_embedding(text: str):
    client = get_bedrock_client()
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": text}),
        contentType="application/json",
        accept="application/json",
    )
    return response
