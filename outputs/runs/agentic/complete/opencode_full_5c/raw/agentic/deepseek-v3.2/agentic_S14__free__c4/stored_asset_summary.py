import boto3
import json
from typing import Optional
from storage_models import SummaryRequest, SummaryResponse


def summarize_content(
    text: str, max_length: int = 200, min_length: int = 50
) -> SummaryResponse:
    """
    Summarize content using AWS Bedrock with Anthropic Claude model.

    Args:
        text: Text content to summarize
        max_length: Maximum length of summary in characters
        min_length: Minimum length of summary in characters

    Returns:
        SummaryResponse with generated summary
    """
    if not text or not text.strip():
        return SummaryResponse(
            success=False,
            error_message="No text provided for summarization",
            provider="aws_bedrock",
        )

    # Truncate text if too long (Bedrock has token limits)
    # Claude 3 has ~200K token context, but we'll be conservative
    if len(text) > 100000:
        text = text[:100000] + "... [truncated]"

    try:
        # Initialize Bedrock runtime client
        bedrock_client = boto3.client("bedrock-runtime")

        # Prepare prompt for Claude
        prompt = f"""Human: Please summarize the following text concisely. 
The summary should be between {min_length} and {max_length} characters.

Text to summarize:
{text}

Assistant: Summary:"""

        # Prepare request body for Claude 3 Sonnet
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}],
        }

        # Call Bedrock with Claude 3 Sonnet model
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body),
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract summary from response
        summary = ""
        for content in response_body.get("content", []):
            if content["type"] == "text":
                summary = content["text"].strip()
                break

        # Clean up summary
        if summary.startswith("Summary:"):
            summary = summary[8:].strip()

        return SummaryResponse(
            success=True,
            summary=summary,
            original_length=len(text),
            summary_length=len(summary),
            provider="aws_bedrock",
        )

    except Exception as e:
        return SummaryResponse(
            success=False, error_message=str(e), provider="aws_bedrock"
        )


def summarize_with_titan(text: str, max_length: int = 200) -> SummaryResponse:
    """
    Alternative summarization using AWS Bedrock Titan model.

    Args:
        text: Text content to summarize
        max_length: Maximum length of summary

    Returns:
        SummaryResponse with generated summary
    """
    if not text or not text.strip():
        return SummaryResponse(
            success=False,
            error_message="No text provided for summarization",
            provider="aws_bedrock_titan",
        )

    try:
        # Initialize Bedrock runtime client
        bedrock_client = boto3.client("bedrock-runtime")

        # Prepare prompt for Titan
        prompt = f"""Please summarize the following text in under {max_length} characters:

{text}

Summary:"""

        # Prepare request body for Titan Text G1 - Express
        request_body = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 300,
                "temperature": 0.2,
                "topP": 0.9,
            },
        }

        # Call Bedrock with Titan model
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-text-express-v1",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body),
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract summary from response
        summary = response_body.get("results", [{}])[0].get("outputText", "").strip()

        # Clean up
        if summary.startswith("Summary:"):
            summary = summary[8:].strip()

        return SummaryResponse(
            success=True,
            summary=summary,
            original_length=len(text),
            summary_length=len(summary),
            provider="aws_bedrock_titan",
        )

    except Exception as e:
        return SummaryResponse(
            success=False, error_message=str(e), provider="aws_bedrock_titan"
        )


def summarize_extracted_document_text(extracted_text: str) -> SummaryResponse:
    """
    Summarize text extracted from a stored document.

    Args:
        extracted_text: Text extracted from document (via OCR or other means)

    Returns:
        SummaryResponse with generated summary
    """
    return summarize_content(extracted_text)


def get_key_points(text: str, num_points: int = 5) -> SummaryResponse:
    """
    Extract key points from text.

    Args:
        text: Text content to analyze
        num_points: Number of key points to extract

    Returns:
        SummaryResponse with key points as summary
    """
    if not text or not text.strip():
        return SummaryResponse(
            success=False,
            error_message="No text provided for key point extraction",
            provider="aws_bedrock",
        )

    try:
        # Initialize Bedrock runtime client
        bedrock_client = boto3.client("bedrock-runtime")

        # Prepare prompt for key point extraction
        prompt = f"""Human: Extract {num_points} key points from the following text. 
Present each key point as a bullet point starting with "- ".

Text:
{text}

Assistant: Key points:"""

        # Prepare request body for Claude
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [{"role": "user", "content": prompt}],
        }

        # Call Bedrock
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(request_body),
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract key points from response
        key_points = ""
        for content in response_body.get("content", []):
            if content["type"] == "text":
                key_points = content["text"].strip()
                break

        return SummaryResponse(
            success=True,
            summary=key_points,
            original_length=len(text),
            summary_length=len(key_points),
            provider="aws_bedrock",
        )

    except Exception as e:
        return SummaryResponse(
            success=False, error_message=str(e), provider="aws_bedrock"
        )


if __name__ == "__main__":
    # Example usage
    sample_text = """Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. Leading AI textbooks define the field as the study of "intelligent agents": any system that perceives its environment and takes actions that maximize its chance of achieving its goals. Some popular accounts use the term "artificial intelligence" to describe machines that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving", however, this definition is rejected by major AI researchers.
    
    AI applications include advanced web search engines (e.g., Google Search), recommendation systems (used by YouTube, Amazon and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative or creative tools (ChatGPT and AI art), automated decision-making and competing at the highest level in strategic game systems (such as chess and Go)."""

    request = SummaryRequest(text=sample_text, max_length=150, min_length=50)
    result = summarize_content(request.text, request.max_length, request.min_length)
    print(f"Summarization result: {result.success}")
    if result.success:
        print(f"Original length: {result.original_length} chars")
        print(f"Summary length: {result.summary_length} chars")
        print(f"Summary: {result.summary}")

    # Get key points
    key_points_result = get_key_points(sample_text, 3)
    print(f"\nKey points result: {key_points_result.success}")
    if key_points_result.success:
        print(f"Key points:\n{key_points_result.summary}")
