import json

from embeddings_client import get_bedrock_client


def embed_batch(payloads, config=None):
    client = get_bedrock_client(config)
    embeddings = []
    for payload in payloads:
        response = client.invoke_model(
            modelId="amazon.titan-embed-text-v2:0",
            body=json.dumps({"inputText": payload["text"]}),
            contentType="application/json",
            accept="application/json"
        )
        stream = response["body"]
        try:
            embeddings.append(json.loads(stream.read())["embedding"])
        finally:
            stream.close()
    return {"embeddings": embeddings}