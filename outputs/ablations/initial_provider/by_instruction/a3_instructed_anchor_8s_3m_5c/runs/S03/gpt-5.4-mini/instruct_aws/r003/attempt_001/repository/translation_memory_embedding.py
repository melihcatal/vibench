import boto3


def embed_translation_segment(text: str, aws_region: str | None = None) -> list[float]:
    client = boto3.client("bedrock-runtime", region_name=aws_region)
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=(f'{"inputText":"{text}"}').encode())
    return []
