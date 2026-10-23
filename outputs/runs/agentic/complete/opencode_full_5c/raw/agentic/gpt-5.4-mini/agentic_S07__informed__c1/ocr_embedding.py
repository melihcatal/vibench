import json

from document_client import bedrock_runtime_client


def embed_document_sections(sections: list[str]) -> list[list[float]]:
    client = bedrock_runtime_client()
    vectors = []
    for section in sections:
        response = client.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            body=json.dumps({"inputText": section}),
            contentType="application/json",
            accept="application/json",
        )
        vectors.append(
            json.loads(response["body"].read().decode("utf-8")).get("embedding", [])
        )
    return vectors
