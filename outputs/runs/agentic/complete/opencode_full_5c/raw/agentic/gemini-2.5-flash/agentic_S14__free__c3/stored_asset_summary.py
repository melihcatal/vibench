from storage_client import get_comprehend_client
from storage_models import StoredAssetSummaryRequest, StoredAssetSummaryResponse
from botocore.exceptions import ClientError


def summarize_stored_asset_content(
    request: StoredAssetSummaryRequest,
) -> StoredAssetSummaryResponse:
    comprehend_client = get_comprehend_client()
    try:
        # AWS Comprehend can be used for various NLP tasks, including summarization (via key phrases or dominant language).
        # For a direct summarization, we might use DetectKeyPhrases as a proxy or other advanced features if available.
        # Note: AWS Comprehend does not have a direct "summarize_text" API like some other LLMs.
        # For this example, we will detect key phrases as a form of content overview/summary.
        response = comprehend_client.detect_key_phrases(
            Text=request.text, LanguageCode=request.language_code
        )
        key_phrases = [phrase["Text"] for phrase in response["KeyPhrases"]]
        summary_text = ". ".join(key_phrases) + "."

        return StoredAssetSummaryResponse(
            success=True,
            message="Content summarized successfully (via key phrases)",
            summary_text=summary_text,
            raw_response=response,
        )
    except ClientError as e:
        return StoredAssetSummaryResponse(
            success=False, message=f"AWS Comprehend ClientError: {e}"
        )
    except Exception as e:
        return StoredAssetSummaryResponse(
            success=False, message=f"An unexpected error occurred: {e}"
        )
