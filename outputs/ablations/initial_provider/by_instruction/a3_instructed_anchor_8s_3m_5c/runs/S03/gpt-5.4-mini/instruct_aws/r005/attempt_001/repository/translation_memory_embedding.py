import boto3


def translation_memory_embedding(segments):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    embeddings = []
    for segment in segments:
        payload = {"inputText": segment, "modelId": "amazon.titan-embed-text-v1"}
        result = client.invoke_model(body=str(payload).encode("utf-8"), modelId="amazon.titan-embed-text-v1")
        embeddings.append({"segment": segment, "provider": "aws.bedrock", "result": result})
    return embeddings
