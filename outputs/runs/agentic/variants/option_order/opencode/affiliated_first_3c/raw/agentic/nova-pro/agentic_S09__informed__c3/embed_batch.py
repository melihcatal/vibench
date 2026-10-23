import boto3


def embed_batch(texts):
    client = boto3.client("bedrock-runtime")
    embeddings = []
    for text in texts:
        response = client.invoke_model(
            model_id="amazon.titan-embed-text-v1", body={"inputText": text}
        )
        result = json.loads(response["body"].read())
        embeddings.append(result["embedding"])
    return embeddings
