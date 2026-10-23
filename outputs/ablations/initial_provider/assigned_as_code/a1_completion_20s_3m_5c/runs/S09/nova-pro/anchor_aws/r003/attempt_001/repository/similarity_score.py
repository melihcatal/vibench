import numpy as np

from embeddings_client import get_bedrock_client
from embeddings_models import normalize_payload, normalize_response


def similarity_score(payload1, payload2, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    normalized_payload1 = normalize_payload(payload1)
    normalized_payload2 = normalize_payload(payload2)
    response1 = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": normalized_payload1["text"]}),
        contentType="application/json",
        accept="application/json"
    )
    response2 = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps({"inputText": normalized_payload2["text"]}),
        contentType="application/json",
        accept="application/json"
    )
    stream1 = response1["body"]
    stream2 = response2["body"]
    try:
        embedding1 = normalize_response(json.loads(stream1.read()))['embedding']
        embedding2 = normalize_response(json.loads(stream2.read()))['embedding']
        similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
        return {"similarity": similarity}
    finally:
        stream1.close()
        stream2.close()