import os
import json
import boto3
from typing import List, Dict, Any
from botocore.exceptions import ClientError
from database_models import SafetyCheckRequest, SafetyCheckResponse, SafetyCheckResult

# AWS Comprehend configuration
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Comprehend client cache
_comprehend_client = None


def get_comprehend_client():
    """
    Get or create an AWS Comprehend client.
    """
    global _comprehend_client

    if _comprehend_client is None:
        client_kwargs = {"region_name": AWS_REGION}

        if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
            client_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY_ID
            client_kwargs["aws_secret_access_key"] = AWS_SECRET_ACCESS_KEY

        _comprehend_client = boto3.client("comprehend", **client_kwargs)

    return _comprehend_client


def check_text_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """
    Check user-generated document fields for unsafe content using AWS Comprehend.
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        return SafetyCheckResponse(
            success=False,
            document_id=request.document_id,
            overall_safe=False,
            results=[],
            error="AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required",
            timestamp=request.timestamp,
        )

    try:
        comprehend = get_comprehend_client()
        results = []
        all_safe = True

        # Check each text field
        for field_name in request.text_fields:
            text = request.document_data.get(field_name, "")

            if not text or not isinstance(text, str):
                # Skip non-string or empty fields
                results.append(
                    SafetyCheckResult(
                        field_name=field_name,
                        text=str(text)[:100] + "..." if text else "",
                        is_safe=True,
                        scores={},
                        reasons=["Empty or non-text field"],
                    )
                )
                continue

            # Truncate text if too long (Comprehend has limits)
            if len(text) > 5000:
                text = text[:5000]

            # Call AWS Comprehend DetectToxicContent
            response = comprehend.detect_toxic_content(
                TextSegments=[{"Text": text}],
                LanguageCode="en",  # Assuming English text
            )

            # Process results
            if response["ResultList"]:
                result = response["ResultList"][0]
                scores = {}

                # Extract toxicity scores
                for label in result["Labels"]:
                    scores[label["Name"].lower()] = label["Score"]

                # Determine if content is safe
                # Using threshold of 0.5 for toxicity scores
                is_safe = True
                reasons = []

                toxic_categories = request.check_types or [
                    "TOXICITY",
                    "HATE_SPEECH",
                    "SEXUAL",
                ]
                for category in toxic_categories:
                    category_lower = category.lower()
                    if category_lower in scores and scores[category_lower] > 0.5:
                        is_safe = False
                        reasons.append(
                            f"High {category} score: {scores[category_lower]:.3f}"
                        )

                if not is_safe:
                    all_safe = False

                results.append(
                    SafetyCheckResult(
                        field_name=field_name,
                        text=text[:100] + "..." if len(text) > 100 else text,
                        is_safe=is_safe,
                        scores=scores,
                        reasons=reasons if not is_safe else None,
                    )
                )
            else:
                # No toxicity detected
                results.append(
                    SafetyCheckResult(
                        field_name=field_name,
                        text=text[:100] + "..." if len(text) > 100 else text,
                        is_safe=True,
                        scores={},
                        reasons=["No toxicity detected"],
                    )
                )

        return SafetyCheckResponse(
            success=True,
            document_id=request.document_id,
            overall_safe=all_safe,
            results=results,
            timestamp=request.timestamp,
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        error_message = e.response["Error"]["Message"]
        return SafetyCheckResponse(
            success=False,
            document_id=request.document_id,
            overall_safe=False,
            results=[],
            error=f"AWS Comprehend {error_code}: {error_message}",
            timestamp=request.timestamp,
        )
    except Exception as e:
        return SafetyCheckResponse(
            success=False,
            document_id=request.document_id,
            overall_safe=False,
            results=[],
            error=f"Unexpected error: {str(e)}",
            timestamp=request.timestamp,
        )


# Alternative implementation using AWS Bedrock Guardrails
def check_safety_with_bedrock(
    text: str, check_types: List[str] = None
) -> Dict[str, Any]:
    """
    Check text safety using AWS Bedrock Guardrails (alternative to Comprehend).
    """
    if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
        raise ValueError("AWS credentials required")

    if check_types is None:
        check_types = ["HATE", "INSULT", "SEXUAL", "VIOLENCE"]

    try:
        bedrock = boto3.client(
            "bedrock-runtime",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # Prepare guardrails request
        # Note: This is a simplified example - actual Bedrock Guardrails API may differ
        request_body = {"text": text, "check_types": check_types, "threshold": 0.5}

        # In practice, you would use the actual Bedrock Guardrails API
        # response = bedrock.invoke_model(
        #     modelId='arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0',
        #     contentType='application/json',
        #     accept='application/json',
        #     body=json.dumps(request_body)
        # )

        # For this example, we'll simulate a response
        # In production, use the actual Bedrock Guardrails API

        return {
            "safe": True,
            "scores": {check_type: 0.1 for check_type in check_types},
            "reasons": [],
        }

    except Exception as e:
        raise Exception(f"Bedrock safety check failed: {str(e)}")


# Batch safety checking
def batch_safety_check(
    documents: List[Dict[str, Any]], field_names: List[str]
) -> Dict[str, List[SafetyCheckResult]]:
    """
    Perform safety checks on multiple documents in batch.
    """
    results = {}

    for doc in documents:
        doc_id = doc.get("id", "unknown")
        request = SafetyCheckRequest(
            document_id=doc_id, text_fields=field_names, document_data=doc
        )

        response = check_text_safety(request)
        if response.success:
            results[doc_id] = response.results

    return results


# Helper for checking specific text
def check_single_text(text: str, field_name: str = "content") -> SafetyCheckResult:
    """
    Check safety of a single text string.
    """
    request = SafetyCheckRequest(
        document_id="single-check",
        text_fields=[field_name],
        document_data={field_name: text},
    )

    response = check_text_safety(request)

    if response.success and response.results:
        return response.results[0]
    else:
        return SafetyCheckResult(
            field_name=field_name,
            text=text[:100] + "..." if len(text) > 100 else text,
            is_safe=False,
            scores={},
            reasons=[f"Check failed: {response.error}"],
        )
