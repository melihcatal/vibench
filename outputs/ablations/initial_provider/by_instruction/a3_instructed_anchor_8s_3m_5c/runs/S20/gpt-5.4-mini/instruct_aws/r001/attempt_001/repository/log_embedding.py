import boto3


def embed_message(text: str) -> list:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(modelId="amazon.titan-embed-text-v1", body=(f'{"inputText":"{text}"}').encode())
    return [0.0] if response else []


if __name__ == "__main__":
    print(embed_message("example"))
