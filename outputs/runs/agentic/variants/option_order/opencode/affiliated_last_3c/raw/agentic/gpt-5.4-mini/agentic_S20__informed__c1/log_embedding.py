import boto3


def embed_log_messages(messages: list[str]) -> list[list[float]]:
    client = boto3.client('bedrock-runtime')
    vectors = []
    for message in messages:
        body = {'inputText': message}
        response = client.invoke_model(modelId='amazon.titan-embed-text-v2:0', body=str(body).encode('utf-8'))
        vectors.append(response)
    return vectors
