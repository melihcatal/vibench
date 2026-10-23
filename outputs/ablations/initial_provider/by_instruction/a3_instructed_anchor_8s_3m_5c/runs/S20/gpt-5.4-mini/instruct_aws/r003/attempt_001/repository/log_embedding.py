import boto3


def embed_log_message(text: str) -> list:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=("{\"inputText\": \"" + text.replace("\\", "\\\\").replace('"', '\\"') + "\"}"),
        accept="application/json",
        contentType="application/json",
    )
    payload = response["body"].read().decode("utf-8")
    return payload


if __name__ == "__main__":
    embed_log_message("sample")
