from storage_client import StorageClient
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse
import boto3
import json
from botocore.exceptions import ClientError


def summarize_stored_asset_content(
    request: StoredAssetSummaryRequest,
) -> StoredAssetSummaryResponse:
    bedrock_runtime_client = StorageClient().get_bedrock_runtime_client()
    model_id = "anthropic.claude-v2"

    try:
        prompt = f"Human: Summarize the following text:\n\n{request.text_content}\n\nAssistant:"
        body = json.dumps(
            {
                "prompt": prompt,
                "max_tokens_to_sample": request.max_tokens,
                "temperature": 0.1,
                "top_p": 0.9,
            }
        )

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        summary = response_body.get("completion")

        return StoredAssetSummaryResponse(
            success=True, summary=summary, message="Content summarized successfully."
        )
    except ClientError as e:
        return StoredAssetSummaryResponse(
            success=False, message=f"Error summarizing content with Bedrock: {e}"
        )
    except Exception as e:
        return StoredAssetSummaryResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
