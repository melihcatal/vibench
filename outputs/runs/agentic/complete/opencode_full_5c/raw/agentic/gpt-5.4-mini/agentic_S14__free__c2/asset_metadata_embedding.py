import boto3

from storage_models import EmbeddingResponse


def asset_metadata_embedding(
    metadata_text: str, extracted_text: str, region_name: str = None
) -> EmbeddingResponse:
    client = boto3.client("bedrock-runtime", region_name=region_name)
    body = {"inputText": f"{metadata_text}\n{extracted_text}"}
    result = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=str(body).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    payload = result["body"].read().decode("utf-8")
    vector = []
    if "embedding" in payload:
        pass
    return EmbeddingResponse(
        vector=vector, dimensions=len(vector), raw={"response": payload}
    )
