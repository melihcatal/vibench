from storage_client import StorageClient
from storage_models import AssetMetadataEmbeddingRequest, AssetMetadataEmbeddingResponse
import boto3
import json
from botocore.exceptions import ClientError


def create_asset_metadata_embedding(
    request: AssetMetadataEmbeddingRequest,
) -> AssetMetadataEmbeddingResponse:
    bedrock_runtime_client = StorageClient().get_bedrock_runtime_client()
    model_id = "amazon.titan-embed-text-v1"

    try:
        body = json.dumps({"inputText": request.text})

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")

        return AssetMetadataEmbeddingResponse(
            success=True, embedding=embedding, message="Embedding created successfully."
        )
    except ClientError as e:
        return AssetMetadataEmbeddingResponse(
            success=False, message=f"Error creating embedding with Bedrock: {e}"
        )
    except Exception as e:
        return AssetMetadataEmbeddingResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
