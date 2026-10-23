from storage_client import get_bedrock_runtime_client
import json


def embed_text(text: str, model_id: str = "amazon.titan-embed-text-v1") -> dict:
    """
    Embeds text (object metadata and extracted text) for search using Amazon Titan Embeddings via Bedrock Runtime.
    """
    bedrock_runtime_client = get_bedrock_runtime_client()
    try:
        body = json.dumps({"inputText": text})

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")

        return {"status": "success", "embedding": embedding}
    except Exception as e:
        return {"status": "error", "message": str(e)}
