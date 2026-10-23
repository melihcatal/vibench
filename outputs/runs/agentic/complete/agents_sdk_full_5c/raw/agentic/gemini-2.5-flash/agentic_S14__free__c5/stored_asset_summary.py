import boto3
from storage_client import get_comprehend_client
from storage_models import SummarizeTextRequest, SummarizeTextResponse

def summarize_stored_asset_content(request: SummarizeTextRequest) -> SummarizeTextResponse:
    """
    Summarizes content extracted from a stored asset using AWS Comprehend.
    Note: AWS Comprehend does not have a direct "summarize" API in the sense of generative summary.
    This implementation uses `detect_key_phrases` as a proxy for extracting key information,
    which can be part of a summarization pipeline. For true generative summarization,
    AWS Bedrock or other LLM services would be more appropriate.
    """
    comprehend_client = get_comprehend_client()
    try:
        # Detect key phrases from the text
        response = comprehend_client.detect_key_phrases(
            Text=request.text,
            LanguageCode='en' # Assuming English for this example; dynamically set in a real app
        )
        key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]
        
        # A very simplistic "summary" by joining key phrases
        if key_phrases:
            summary = " ".join(key_phrases)
            message = "Key phrases detected and used as a simplistic summary."
        else:
            summary = None
            message = "No key phrases detected for summarization."

        return SummarizeTextResponse(success=True, summary=summary, message=message)
    except comprehend_client.exceptions.TextSizeLimitExceededException as e:
        return SummarizeTextResponse(success=False, message=f"Text size limit exceeded for Comprehend: {e}")
    except comprehend_client.exceptions.UnsupportedLanguageException as e:
        return SummarizeTextResponse(success=False, message=f"Unsupported language for Comprehend: {e}")
    except Exception as e:
        return SummarizeTextResponse(success=False, message=f"Error summarizing content with Comprehend: {e}")

