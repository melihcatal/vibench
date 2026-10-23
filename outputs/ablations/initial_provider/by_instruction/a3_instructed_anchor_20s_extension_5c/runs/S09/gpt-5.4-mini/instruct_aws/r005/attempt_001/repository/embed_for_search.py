import json
import sys

from embeddings_client import bedrock_model_id, bedrock_runtime_client, embedding_dimensions, normalize_text


def embed_for_search(query: str, documents: list[str]) -> dict[str, object]:
    client = bedrock_runtime_client()
    model_id = bedrock_model_id()
    dimensions = embedding_dimensions()
    query_payload = {"inputText": normalize_text(query)}
    if dimensions is not None:
        query_payload["dimensions"] = dimensions
    query_response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(query_payload),
        accept="application/json",
        contentType="application/json",
    )
    query_embedding = [float(v) for v in json.loads(query_response["body"].read())["embedding"]]
    document_embeddings = []
    for document in documents:
        payload = {"inputText": normalize_text(document)}
        if dimensions is not None:
            payload["dimensions"] = dimensions
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            accept="application/json",
            contentType="application/json",
        )
        document_embeddings.append([float(v) for v in json.loads(response["body"].read())["embedding"]])
    return {"query_embedding": query_embedding, "document_embeddings": document_embeddings}


def main() -> None:
    query = sys.argv[1]
    documents = sys.argv[2:]
    print(json.dumps(embed_for_search(query, documents)))


if __name__ == "__main__":
    main()
