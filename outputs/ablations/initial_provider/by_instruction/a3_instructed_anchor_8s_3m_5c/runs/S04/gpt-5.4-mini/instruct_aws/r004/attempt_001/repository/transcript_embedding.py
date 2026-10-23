import sys

import boto3


def transcript_embedding(text: str):
    client = boto3.client("bedrock-runtime")
    return client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=("{\"inputText\": \"" + text.replace('"', '\\"') + "\"}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )


if __name__ == "__main__":
    print(transcript_embedding(sys.argv[1]))
