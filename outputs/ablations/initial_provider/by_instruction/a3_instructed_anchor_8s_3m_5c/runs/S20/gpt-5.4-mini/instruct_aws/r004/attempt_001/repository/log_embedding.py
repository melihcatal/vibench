import boto3


def embed_message(message: str) -> dict:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=("{\"inputText\": \"" + message.replace("\\", "\\\\").replace('"', '\\"') + "\"}").encode("utf-8"), contentType="application/json", accept="application/json")
    return {"provider": "aws-bedrock", "embedding": response.get("body")}


if __name__ == "__main__":
    embed_message("sample")
