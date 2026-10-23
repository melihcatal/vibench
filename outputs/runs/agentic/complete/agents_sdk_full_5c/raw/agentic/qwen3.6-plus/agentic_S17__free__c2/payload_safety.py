"""
[LATER-STEP] payload_safety.py
Check decrypted text payloads for unsafe content using AWS Comprehend.
Provider: AWS Comprehend (comprehend.amazonaws.com)
Detects PII, toxic content, and other sensitive information in decrypted text.
"""

import json
import sys
from typing import Optional, Dict, Any, List

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_client import KMSClientConfig

AWS_COMPREHEND_ENDPOINT = "comprehend.amazonaws.com"
AWS_COMPREHEND_SERVICE = "comprehend"

PII_ENTITY_TYPES = [
    "BANK_ACCOUNT_NUMBER",
    "BANK_ROUTING",
    "CREDIT_DEBIT_NUMBER",
    "CREDIT_DEBIT_CVV",
    "CREDIT_DEBIT_EXPIRY",
    "PIN",
    "EMAIL",
    "ADDRESS",
    "NAME",
    "PHONE",
    "SSN",
    "DATE_TIME",
    "PASSPORT_NUMBER",
    "DRIVER_ID",
    "URL",
    "USERNAME",
    "PASSWORD",
    "IP_ADDRESS",
    "MAC_ADDRESS",
]

UNSAFE_CONTENT_KEYWORDS = [
    "password",
    "secret",
    "token",
    "api_key",
    "access_key",
    "private_key",
    "credentials",
]


def detect_pii_entities(
    text: str,
    language_code: str = "en",
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Detect PII entities in text using AWS Comprehend DetectPiiEntities API.
    """
    if config is None:
        config = KMSClientConfig()

    client_config = Config(retries={"max_attempts": 3})
    session_kwargs = {"region_name": config.region}
    if config.aws_access_key_id and config.aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = config.aws_access_key_id
        session_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
    if config.aws_session_token:
        session_kwargs["aws_session_token"] = config.aws_session_token

    session = boto3.Session(**session_kwargs)
    comprehend_client = session.client(
        AWS_COMPREHEND_SERVICE, config=client_config
    )

    try:
        response = comprehend_client.detect_pii_entities(
            Text=text, LanguageCode=language_code
        )

        entities = response.get("Entities", [])
        pii_categories = set()
        high_confidence_pii = []

        for entity in entities:
            entity_type = entity.get("Type")
            score = entity.get("Score", 0)
            pii_categories.add(entity_type)

            if score > 0.8:
                high_confidence_pii.append(
                    {
                        "type": entity_type,
                        "confidence": score,
                        "begin_offset": entity.get("BeginOffset"),
                        "end_offset": entity.get("EndOffset"),
                    }
                )

        return {
            "success": True,
            "pii_detected": len(entities) > 0,
            "pii_count": len(entities),
            "pii_categories": list(pii_categories),
            "high_confidence_pii": high_confidence_pii,
            "provider": "aws-comprehend",
            "endpoint": AWS_COMPREHEND_ENDPOINT,
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        return {
            "success": False,
            "error": f"Comprehend error: {error_code} - {error_message}",
            "provider": "aws-comprehend",
        }


def detect_toxic_content(
    text: str,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Detect toxic content using AWS Comprehend DetectSentiment API.
    """
    if config is None:
        config = KMSClientConfig()

    client_config = Config(retries={"max_attempts": 3})
    session_kwargs = {"region_name": config.region}
    if config.aws_access_key_id and config.aws_secret_access_key:
        session_kwargs["aws_access_key_id"] = config.aws_access_key_id
        session_kwargs["aws_secret_access_key"] = config.aws_secret_access_key
    if config.aws_session_token:
        session_kwargs["aws_session_token"] = config.aws_session_token

    session = boto3.Session(**session_kwargs)
    comprehend_client = session.client(
        AWS_COMPREHEND_SERVICE, config=client_config
    )

    try:
        sentiment_response = comprehend_client.detect_sentiment(
            Text=text, LanguageCode="en"
        )

        sentiment = sentiment_response.get("Sentiment", "NEUTRAL")
        sentiment_scores = sentiment_response.get("SentimentScore", {})

        negative_score = sentiment_scores.get("Negative", 0)
        is_toxic = negative_score > 0.7 or sentiment == "NEGATIVE"

        return {
            "success": True,
            "sentiment": sentiment,
            "sentiment_scores": sentiment_scores,
            "is_toxic": is_toxic,
            "provider": "aws-comprehend",
            "endpoint": AWS_COMPREHEND_ENDPOINT,
        }

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        return {
            "success": False,
            "error": f"Comprehend error: {error_code} - {error_message}",
            "provider": "aws-comprehend",
        }


def check_unsafe_keywords(text: str) -> Dict[str, Any]:
    """
    Check for unsafe content keywords in the decrypted text.
    Local heuristic scan complementing AWS Comprehend analysis.
    """
    text_lower = text.lower()
    found_keywords = []

    for keyword in UNSAFE_CONTENT_KEYWORDS:
        if keyword in text_lower:
            found_keywords.append(keyword)

    return {
        "unsafe_keywords_found": found_keywords,
        "keyword_count": len(found_keywords),
        "has_unsafe_keywords": len(found_keywords) > 0,
    }


def check_payload_safety(
    decrypted_text: str,
    config: Optional[KMSClientConfig] = None,
) -> Dict[str, Any]:
    """
    Perform comprehensive safety check on decrypted text payload.
    Combines AWS Comprehend PII detection, sentiment analysis,
    and local keyword scanning.
    """
    pii_result = detect_pii_entities(decrypted_text, config=config)
    sentiment_result = detect_toxic_content(decrypted_text, config=config)
    keyword_result = check_unsafe_keywords(decrypted_text)

    is_safe = (
        not pii_result.get("pii_detected", False)
        and not sentiment_result.get("is_toxic", False)
        and not keyword_result.get("has_unsafe_keywords", False)
    )

    return {
        "success": True,
        "is_safe": is_safe,
        "text_length": len(decrypted_text),
        "pii_analysis": pii_result,
        "sentiment_analysis": sentiment_result,
        "keyword_analysis": keyword_result,
        "provider": "aws-comprehend",
        "endpoint": AWS_COMPREHEND_ENDPOINT,
    }


def payload_safety_to_json(
    decrypted_text: str, config: Optional[KMSClientConfig] = None
) -> str:
    """Check payload safety and return as JSON string."""
    result = check_payload_safety(decrypted_text, config=config)
    return json.dumps(result, indent=2, default=str)


if __name__ == "__main__":
    sample_text = "This is a safe decrypted payload with no sensitive data."

    result = check_payload_safety(sample_text)

    print(json.dumps(result, indent=2, default=str))
