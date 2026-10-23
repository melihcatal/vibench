import os
import re
import json
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError
from openai import OpenAI


def check_payload_safety(plaintext: str, provider: str = "openai") -> Dict[str, Any]:
    """
    Check decrypted text payloads for unsafe content using AI content moderation.

    Args:
        plaintext: The decrypted plaintext to check
        provider: Content moderation provider ('openai', 'aws', or 'google')

    Returns:
        Dictionary with safety analysis results
    """
    if provider == "openai":
        return _check_with_openai(plaintext)
    elif provider == "aws":
        return _check_with_aws(plaintext)
    elif provider == "google":
        return _check_with_google(plaintext)
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def _check_with_openai(plaintext: str) -> Dict[str, Any]:
    """Check content safety using OpenAI moderation API."""
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Call OpenAI moderation endpoint
        response = client.moderations.create(
            model="text-moderation-latest", input=plaintext
        )

        moderation = response.results[0]

        # Extract categories and scores
        categories = moderation.categories
        category_scores = moderation.category_scores

        # Determine overall safety
        flagged = moderation.flagged
        highest_score = max(
            [
                getattr(category_scores, attr)
                for attr in dir(category_scores)
                if not attr.startswith("_")
                and not callable(getattr(category_scores, attr))
            ]
        )

        # Check for specific patterns
        pattern_checks = _perform_pattern_checks(plaintext)

        # Prepare safety report
        safety_report = {
            "flagged": flagged,
            "categories_flagged": [
                cat
                for cat, flagged in categories.__dict__.items()
                if not cat.startswith("_") and flagged
            ],
            "category_scores": {
                cat: getattr(category_scores, cat)
                for cat in dir(category_scores)
                if not cat.startswith("_")
                and not callable(getattr(category_scores, cat))
            },
            "highest_risk_score": highest_score,
            "risk_level": _determine_risk_level(highest_score),
            "pattern_checks": pattern_checks,
            "provider": "openai",
            "model": "text-moderation-latest",
            "analysis_timestamp": os.environ.get("ANALYSIS_TIMESTAMP", ""),
        }

        return safety_report

    except Exception as e:
        raise Exception(f"OpenAI content moderation failed: {str(e)}")


def _check_with_aws(plaintext: str) -> Dict[str, Any]:
    """Check content safety using AWS Comprehend."""
    try:
        # Initialize AWS Comprehend client
        comprehend_client = boto3.client(
            "comprehend", region_name=os.environ.get("AWS_REGION", "us-east-1")
        )

        # Detect PII entities
        pii_response = comprehend_client.detect_pii_entities(
            Text=plaintext, LanguageCode="en"
        )

        # Detect sentiment (as proxy for toxicity)
        sentiment_response = comprehend_client.detect_sentiment(
            Text=plaintext, LanguageCode="en"
        )

        # Check for specific patterns
        pattern_checks = _perform_pattern_checks(plaintext)

        # Extract PII entities
        pii_entities = []
        for entity in pii_response.get("Entities", []):
            pii_entities.append(
                {
                    "type": entity["Type"],
                    "score": entity["Score"],
                    "text": plaintext[entity["BeginOffset"] : entity["EndOffset"]],
                }
            )

        # Prepare safety report
        safety_report = {
            "pii_detected": len(pii_entities) > 0,
            "pii_entities": pii_entities,
            "sentiment": {
                "overall": sentiment_response["Sentiment"],
                "scores": sentiment_response["SentimentScore"],
            },
            "pattern_checks": pattern_checks,
            "risk_level": _determine_aws_risk_level(
                pii_entities, sentiment_response["Sentiment"]
            ),
            "provider": "aws_comprehend",
            "analysis_timestamp": os.environ.get("ANALYSIS_TIMESTAMP", ""),
        }

        return safety_report

    except ClientError as e:
        raise Exception(f"AWS Comprehend content check failed: {str(e)}")


def _check_with_google(plaintext: str) -> Dict[str, Any]:
    """Check content safety using Google Perspective API."""
    try:
        # Note: Google Perspective API requires different setup
        # This is a placeholder implementation
        from googleapiclient import discovery
        import google.auth

        # Initialize Google API client
        API_KEY = os.environ.get("GOOGLE_API_KEY")

        # This would require proper Google Cloud setup
        # For now, we'll use pattern checks

        # Check for specific patterns
        pattern_checks = _perform_pattern_checks(plaintext)

        # Prepare safety report
        safety_report = {
            "pattern_checks": pattern_checks,
            "provider": "google_perspective",
            "analysis_timestamp": os.environ.get("ANALYSIS_TIMESTAMP", ""),
            "note": "Google Perspective API integration requires additional setup",
        }

        return safety_report

    except ImportError:
        # Fall back to pattern checks only
        pattern_checks = _perform_pattern_checks(plaintext)

        return {
            "pattern_checks": pattern_checks,
            "provider": "pattern_only",
            "analysis_timestamp": os.environ.get("ANALYSIS_TIMESTAMP", ""),
            "note": "Google API not available, using pattern checks only",
        }
    except Exception as e:
        raise Exception(f"Google content check failed: {str(e)}")


def _perform_pattern_checks(text: str) -> Dict[str, Any]:
    """Perform regex pattern checks for unsafe content."""
    patterns = {
        "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
        "ssn": r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "malicious_url": r"(?:https?://)?(?:www\.)?(?:malware|phishing|exploit|attack)\.[a-z]{2,}",
        "sql_injection": r"(?:union\s+select|select\s+.+from|insert\s+into|update\s+.+set|delete\s+from|drop\s+table)",
        "xss": r"(?:<script>|javascript:|onload=|onerror=|onclick=)",
        "command_injection": r"(?:;\s*(?:rm|ls|cat|echo|wget|curl)\s+|`.*`|\$\(.*\))",
    }

    results = {}
    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        results[pattern_name] = {
            "detected": len(matches) > 0,
            "match_count": len(matches),
            "matches": matches[:5],  # Limit to first 5 matches
        }

    # Calculate overall pattern risk
    high_risk_patterns = [
        "credit_card",
        "ssn",
        "sql_injection",
        "xss",
        "command_injection",
    ]
    high_risk_detected = any(
        results[pattern]["detected"] for pattern in high_risk_patterns
    )

    results["overall_pattern_risk"] = {
        "high_risk_detected": high_risk_detected,
        "total_matches": sum(results[pattern]["match_count"] for pattern in patterns),
        "sensitive_data_detected": results["credit_card"]["detected"]
        or results["ssn"]["detected"],
        "injection_attempts": results["sql_injection"]["detected"]
        or results["xss"]["detected"]
        or results["command_injection"]["detected"],
    }

    return results


def _determine_risk_level(score: float) -> str:
    """Determine risk level based on score."""
    if score >= 0.9:
        return "CRITICAL"
    elif score >= 0.7:
        return "HIGH"
    elif score >= 0.5:
        return "MEDIUM"
    elif score >= 0.3:
        return "LOW"
    else:
        return "SAFE"


def _determine_aws_risk_level(pii_entities: List[Dict], sentiment: str) -> str:
    """Determine risk level for AWS analysis."""
    sensitive_pii = any(
        entity["type"] in ["SSN", "CREDIT_DEBIT_NUMBER", "BANK_ACCOUNT_NUMBER"]
        for entity in pii_entities
    )

    if sensitive_pii:
        return "HIGH"
    elif len(pii_entities) > 0:
        return "MEDIUM"
    elif sentiment in ["NEGATIVE", "MIXED"]:
        return "LOW"
    else:
        return "SAFE"


def validate_decrypted_payload(
    decryption_result: Dict[str, Any], safety_provider: str = "openai"
) -> Dict[str, Any]:
    """
    Validate a decrypted payload including safety checks.

    Args:
        decryption_result: Result from decrypt_payload function
        safety_provider: Provider to use for safety checks

    Returns:
        Dictionary with validation results
    """
    try:
        # Extract plaintext
        if isinstance(decryption_result, dict) and "plaintext" in decryption_result:
            plaintext = decryption_result["plaintext"]
        elif isinstance(decryption_result, str):
            plaintext = decryption_result
        else:
            raise ValueError("Invalid decryption result format")

        # Perform safety check
        safety_result = check_payload_safety(plaintext, safety_provider)

        # Perform additional validation
        validation_checks = {
            "empty_content": len(plaintext.strip()) == 0,
            "excessive_length": len(plaintext) > 1000000,  # 1MB
            "binary_content": any(
                ord(c) < 32 and c not in "\n\r\t" for c in plaintext[:100]
            ),
            "encoding_issues": not all(
                ord(c) < 128 for c in plaintext[:1000]
            ),  # Check for non-ASCII
        }

        # Prepare validation report
        validation_report = {
            "payload_metadata": {
                "length": len(plaintext),
                "first_100_chars": plaintext[:100],
                "is_empty": validation_checks["empty_content"],
            },
            "safety_analysis": safety_result,
            "validation_checks": validation_checks,
            "overall_validation": {
                "passed": not safety_result.get("flagged", False)
                and not validation_checks["excessive_length"]
                and not validation_checks["binary_content"],
                "warnings": [
                    check for check, failed in validation_checks.items() if failed
                ],
                "risk_level": safety_result.get("risk_level", "UNKNOWN"),
            },
            "provider": safety_provider,
            "validation_timestamp": os.environ.get("VALIDATION_TIMESTAMP", ""),
        }

        return validation_report

    except Exception as e:
        raise Exception(f"Payload validation failed: {str(e)}")
