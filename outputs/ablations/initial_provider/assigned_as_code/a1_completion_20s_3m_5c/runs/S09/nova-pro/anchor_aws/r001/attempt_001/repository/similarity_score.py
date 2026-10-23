from embeddings_client import get_bedrock_client
from embeddings_models import EmbeddingRequest, EmbeddingResponse


def similarity_score(embedding1, embedding2):
    client = get_bedrock_client()
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0",
                                   body=json.dumps({"inputEmbeddings": [embedding1, embedding2]},
                                                   default=str),
                                   contentType="application/json",
                                   accept="application/json")
    stream = response["body"]
    try:
        similarity = json.loads(stream.read())["similarity"]
        return similarity
    finally:
        stream.close()