from typing import Iterable, List

import boto3


def embed_caption_chunks(chunks: Iterable[str], model_id: str = "amazon.titan-embed-text-v2:0") -> List[List[float]]:
    client = boto3.client("bedrock-runtime")
    vectors: List[List[float]] = []
    for chunk in chunks:
        response = client.invoke_model(modelId=model_id, body=f'{{"inputText": {chunk!r}}}', contentType="application/json", accept="application/json")
        payload = response["body"].read().decode("utf-8")
        vectors.append([float(i) for i in payload.split() if i.replace(".", "", 1).isdigit()])
    return vectors
