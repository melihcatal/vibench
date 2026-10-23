import os
import json
import re
from typing import Dict, List, Any, Optional, Tuple
import boto3
from botocore.exceptions import ClientError


def check_payload_safety(plaintext, check_types=None):
    """
    Check decrypted text payloads for unsafe content using AWS Comprehend.

    Args:
        plaintext: Decrypted plaintext to check
        check_types: List of check types to perform

    Returns:
        dict with safety analysis results
    """
    if isinstance(plaintext, bytes):
        try:
            plaintext_str = plaintext.decode("utf-8")
        except UnicodeDecodeError:
            return {
                "safe": False,
                "reason": "binary_data",
                "details": "Payload is binary data, cannot analyze text safety",
                "provider": "aws_comprehend",
            }
    else:
        plaintext_str = str(plaintext)

    if check_types is None:
        check_types = ["pii", "toxicity", "sentiment"]

    comprehend_client = boto3.client(
        "comprehend", region_name=os.environ.get("AWS_REGION", "us-east-1")
    )

    results = {
        "payload_preview": plaintext_str[:100]
        + ("..." if len(plaintext_str) > 100 else ""),
        "total_length": len(plaintext_str),
        "checks_performed": check_types,
        "provider": "aws_comprehend",
        "results": {},
    }

    try:
        if "pii" in check_types:
            pii_response = comprehend_client.detect_pii_entities(
                Text=plaintext_str[:5000], LanguageCode="en"
            )
            pii_entities = pii_response.get("Entities", [])
            results["results"]["pii"] = {
                "entities_found": len(pii_entities),
                "entities": [
                    {
                        "type": entity.get("Type"),
                        "score": entity.get("Score"),
                        "text": plaintext_str[
                            entity.get("BeginOffset", 0) : entity.get("EndOffset", 0)
                        ],
                    }
                    for entity in pii_entities
                ],
            }

        if "toxicity" in check_types:
            try:
                toxicity_response = comprehend_client.detect_toxic_content(
                    TextSegments=[{"Text": plaintext_str[:1000]}], LanguageCode="en"
                )
                toxicity_results = toxicity_response.get("ResultList", [])
                if toxicity_results:
                    toxicity_scores = toxicity_results[0].get("Labels", [])
                    results["results"]["toxicity"] = {
                        "scores": [
                            {"name": label.get("Name"), "score": label.get("Score")}
                            for label in toxicity_scores
                        ],
                        "highest_toxicity": max(
                            [label.get("Score", 0) for label in toxicity_scores],
                            default=0,
                        ),
                    }
            except ClientError:
                results["results"]["toxicity"] = {
                    "error": "Toxic content detection not available in this region"
                }

        if "sentiment" in check_types:
            sentiment_response = comprehend_client.detect_sentiment(
                Text=plaintext_str[:5000], LanguageCode="en"
            )
            results["results"]["sentiment"] = {
                "sentiment": sentiment_response.get("Sentiment"),
                "scores": sentiment_response.get("SentimentScore", {}),
            }

        if "key_phrases" in check_types:
            key_phrases_response = comprehend_client.detect_key_phrases(
                Text=plaintext_str[:5000], LanguageCode="en"
            )
            key_phrases = key_phrases_response.get("KeyPhrases", [])
            results["results"]["key_phrases"] = {
                "phrases_found": len(key_phrases),
                "phrases": [
                    {"text": phrase.get("Text"), "score": phrase.get("Score")}
                    for phrase in key_phrases
                ],
            }

        safety_score = calculate_safety_score(results["results"])
        results["safety_score"] = safety_score
        results["safe"] = safety_score >= 0.7

        return results

    except ClientError as e:
        raise Exception(f"AWS Comprehend analysis failed: {e}")


def calculate_safety_score(results: Dict[str, Any]) -> float:
    """Calculate overall safety score from analysis results."""
    score = 1.0

    if "pii" in results:
        pii_entities = results["pii"].get("entities_found", 0)
        if pii_entities > 0:
            score -= min(0.3, pii_entities * 0.1)

    if "toxicity" in results:
        toxicity = results["toxicity"].get("highest_toxicity", 0)
        if toxicity > 0.7:
            score -= 0.4
        elif toxicity > 0.4:
            score -= 0.2

    if "sentiment" in results:
        sentiment = results["sentiment"].get("sentiment", "NEUTRAL")
        if sentiment == "NEGATIVE":
            score -= 0.1

    return max(0.0, min(1.0, score))


def check_for_sensitive_patterns(text: str) -> Dict[str, Any]:
    """Check for sensitive patterns using regex."""
    patterns = {
        "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
        "ssn": r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b",
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
        "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "secret_key": r"\b(?:secret|key|token|password)[:=]\s*[\w\-]+\b",
        "jwt": r"\beyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\b",
    }

    findings = {}
    for pattern_name, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            findings[pattern_name] = {"count": len(matches), "examples": matches[:3]}

    return {
        "pattern_check": True,
        "findings": findings,
        "total_findings": sum(finding["count"] for finding in findings.values()),
    }


def analyze_decrypted_payload(
    decryption_result, safety_checks=True, pattern_checks=True
):
    """
    Analyze a decrypted payload for safety and compliance.

    Args:
        decryption_result: Result from decrypt_payload or envelope_decrypt
        safety_checks: Whether to perform AWS Comprehend safety checks
        pattern_checks: Whether to perform regex pattern checks

    Returns:
        Comprehensive analysis result
    """
    plaintext = decryption_result.get("plaintext")
    plaintext_str = decryption_result.get("plaintext_str")

    if plaintext_str is None and isinstance(plaintext, bytes):
        try:
            plaintext_str = plaintext.decode("utf-8")
        except UnicodeDecodeError:
            plaintext_str = None

    analysis = {
        "decryption_metadata": {
            "key_id": decryption_result.get("key_id"),
            "provider": decryption_result.get("provider", "aws_kms"),
            "context": decryption_result.get("encryption_context", {}),
        },
        "payload_info": {
            "is_text": plaintext_str is not None,
            "length_bytes": len(plaintext) if plaintext else 0,
            "preview": plaintext_str[:200]
            + ("..." if plaintext_str and len(plaintext_str) > 200 else "")
            if plaintext_str
            else "Binary data",
        },
        "safety_analysis": None,
        "pattern_analysis": None,
        "overall_safety": "unknown",
    }

    if safety_checks and plaintext_str:
        try:
            safety_result = check_payload_safety(plaintext_str)
            analysis["safety_analysis"] = safety_result
            analysis["overall_safety"] = (
                "safe" if safety_result.get("safe", False) else "unsafe"
            )
        except Exception as e:
            analysis["safety_analysis"] = {"error": str(e)}

    if pattern_checks and plaintext_str:
        pattern_result = check_for_sensitive_patterns(plaintext_str)
        analysis["pattern_analysis"] = pattern_result

        if pattern_result.get("total_findings", 0) > 0:
            if analysis["overall_safety"] == "safe":
                analysis["overall_safety"] = "sensitive_patterns_found"
            elif analysis["overall_safety"] == "unknown":
                analysis["overall_safety"] = "sensitive_patterns_found"

    if analysis["overall_safety"] == "unknown" and plaintext_str:
        analysis["overall_safety"] = "no_issues_detected"

    return analysis


if __name__ == "__main__":
    test_text = (
        "This is a test payload with email test@example.com and phone 555-123-4567."
    )
    safety_result = check_payload_safety(test_text)
    print(f"Safety analysis: {json.dumps(safety_result, indent=2)}")
