import json
from storage_client import get_bedrock_runtime_client
from storage_models import EmbedMetadataRequest, EmbedMetadataResponse


def embed_asset_metadata_and_text(
    request: EmbedMetadataRequest,
) -> EmbedMetadataResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()
    try:
        body = json.dumps({"inputText": request.text})
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId="amazon.titan-embed-text-v1",
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")

        return EmbedMetadataResponse(
            success=True, message="Text embedded successfully.", embedding=embedding
        )
    except Exception as e:
        return EmbedMetadataResponse(
            success=False, message=f"Error embedding text: {str(e)}"
        )
