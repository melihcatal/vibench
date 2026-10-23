import os
import re
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import boto3
from botocore.exceptions import ClientError


@dataclass
class SafetyCheckResult:
    """Result of payload safety check."""

    safe: bool
    checks_passed: List[str]
    checks_failed: List[str]
    warnings: List[str]
    confidence_score: float
    provider: str = "aws_comprehend"


class PayloadSafetyChecker:
    """Check decrypted text payloads for unsafe content using AWS Comprehend."""

    def __init__(self, region: Optional[str] = None):
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self.comprehend = boto3.client("comprehend", region_name=self.region)

        # Local pattern matching for quick checks
        self.sensitive_patterns = [
            r"\b\d{3}[-.]?\d{2}[-.]?\d{4}\b",  # SSN
            r"\b\d{16}\b",  # Credit card (16 digits)
            r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Credit card with separators
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
            r"\b\d{10}\b",  # Phone number (10 digits)
            r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",  # Phone number with separators
        ]

        self.threat_keywords = [
            "exploit",
            "vulnerability",
            "attack",
            "malware",
            "ransomware",
            "backdoor",
            "trojan",
            "virus",
            "worm",
            "keylogger",
            "spyware",
            "phishing",
            "brute force",
            "ddos",
            "sql injection",
            "xss",
            "zero-day",
            "payload",
            "shellcode",
            "rootkit",
        ]

    def check_with_comprehend(self, text: str) -> Dict[str, Any]:
        """
        Use AWS Comprehend to detect PII and unsafe content.

        Args:
            text: Text to analyze

        Returns:
            Comprehend analysis results
        """
        try:
            # Detect PII entities
            pii_response = self.comprehend.detect_pii_entities(
                Text=text, LanguageCode="en"
            )

            # Detect sentiment (negative sentiment might indicate unsafe content)
            sentiment_response = self.comprehend.detect_sentiment(
                Text=text, LanguageCode="en"
            )

            # Detect key phrases
            key_phrases_response = self.comprehend.detect_key_phrases(
                Text=text, LanguageCode="en"
            )

            return {
                "pii_entities": pii_response["Entities"],
                "sentiment": sentiment_response["Sentiment"],
                "sentiment_scores": sentiment_response["SentimentScore"],
                "key_phrases": [
                    kp["Text"] for kp in key_phrases_response["KeyPhrases"]
                ],
                "provider": "aws_comprehend",
            }
        except ClientError as e:
            raise Exception(f"AWS Comprehend analysis failed: {e}")

    def check_local_patterns(self, text: str) -> Dict[str, Any]:
        """
        Check for sensitive patterns using local regex patterns.

        Args:
            text: Text to check

        Returns:
            Pattern matching results
        """
        results = {
            "sensitive_patterns_found": [],
            "threat_keywords_found": [],
            "provider": "local_patterns",
        }

        # Check for sensitive patterns
        for pattern in self.sensitive_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                pattern_name = (
                    pattern.replace("\\b", "").replace("\\d", "d").replace("[A-Z]", "A")
                )
                results["sensitive_patterns_found"].append(
                    {
                        "pattern": pattern_name[:50],
                        "matches": matches[:5],  # Limit matches for output
                        "count": len(matches),
                    }
                )

        # Check for threat keywords
        text_lower = text.lower()
        for keyword in self.threat_keywords:
            if keyword.lower() in text_lower:
                results["threat_keywords_found"].append(keyword)

        return results

    def check_payload_safety(
        self, decrypted_text: str, use_comprehend: bool = True
    ) -> SafetyCheckResult:
        """
        Comprehensive safety check for decrypted payloads.

        Args:
            decrypted_text: The decrypted text to check
            use_comprehend: Whether to use AWS Comprehend (requires permissions)

        Returns:
            SafetyCheckResult with detailed findings
        """
        checks_passed = []
        checks_failed = []
        warnings = []
        confidence_score = 1.0

        # Check 1: Empty or very short text
        if not decrypted_text or len(decrypted_text.strip()) < 3:
            checks_failed.append("payload_too_short")
            confidence_score *= 0.5
        else:
            checks_passed.append("payload_length_ok")

        # Check 2: Local pattern matching
        local_results = self.check_local_patterns(decrypted_text)

        if local_results["sensitive_patterns_found"]:
            checks_failed.append("sensitive_patterns_detected")
            for pattern in local_results["sensitive_patterns_found"]:
                warnings.append(
                    f"Found {pattern['count']} matches for pattern: {pattern['pattern']}"
                )
            confidence_score *= 0.3

        if local_results["threat_keywords_found"]:
            checks_failed.append("threat_keywords_detected")
            warnings.append(
                f"Found threat keywords: {', '.join(local_results['threat_keywords_found'][:3])}"
            )
            confidence_score *= 0.4

        if (
            not local_results["sensitive_patterns_found"]
            and not local_results["threat_keywords_found"]
        ):
            checks_passed.append("local_patterns_clean")

        # Check 3: AWS Comprehend analysis (if enabled)
        comprehend_results = None
        if use_comprehend:
            try:
                comprehend_results = self.check_with_comprehend(decrypted_text)

                # Check for PII entities
                if comprehend_results["pii_entities"]:
                    checks_failed.append("pii_entities_detected")
                    pii_types = set(
                        entity["Type"] for entity in comprehend_results["pii_entities"]
                    )
                    warnings.append(
                        f"AWS Comprehend detected PII types: {', '.join(pii_types)}"
                    )
                    confidence_score *= 0.2
                else:
                    checks_passed.append("no_pii_detected")

                # Check sentiment
                sentiment = comprehend_results["sentiment"]
                sentiment_scores = comprehend_results["sentiment_scores"]

                if sentiment == "NEGATIVE" and sentiment_scores["Negative"] > 0.7:
                    checks_failed.append("high_negative_sentiment")
                    warnings.append(
                        f"High negative sentiment detected: {sentiment_scores['Negative']:.2f}"
                    )
                    confidence_score *= 0.8

                checks_passed.append("comprehend_analysis_complete")

            except Exception as e:
                warnings.append(f"AWS Comprehend check skipped: {str(e)}")
                checks_failed.append("comprehend_unavailable")
                confidence_score *= 0.9

        # Check 4: Binary or encoded content detection
        try:
            # Try to decode as JSON to check structure
            json.loads(decrypted_text)
            checks_passed.append("valid_json_structure")
        except json.JSONDecodeError:
            # Not JSON, check for other structures
            if decrypted_text.startswith(("{", "[", "<")):
                warnings.append("Payload appears to be structured but not valid JSON")

        # Check 5: Size limits
        text_length = len(decrypted_text)
        if text_length > 100000:  # 100KB
            warnings.append(f"Large payload size: {text_length} characters")
            confidence_score *= 0.9

        # Determine overall safety
        unsafe_checks = [
            "sensitive_patterns_detected",
            "threat_keywords_detected",
            "pii_entities_detected",
            "high_negative_sentiment",
        ]

        is_safe = not any(check in checks_failed for check in unsafe_checks)

        return SafetyCheckResult(
            safe=is_safe,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            warnings=warnings,
            confidence_score=round(confidence_score, 2),
            provider="aws_comprehend" if comprehend_results else "local_patterns",
        )

    def generate_safety_report(
        self, decrypted_text: str, metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a detailed safety report for a decrypted payload.

        Args:
            decrypted_text: The decrypted text
            metadata: Additional metadata about the payload

        Returns:
            Comprehensive safety report
        """
        safety_result = self.check_payload_safety(decrypted_text)

        report = {
            "timestamp": os.getenv("REQUEST_TIMESTAMP", ""),
            "payload_size": len(decrypted_text),
            "safety_result": {
                "safe": safety_result.safe,
                "confidence_score": safety_result.confidence_score,
                "checks_passed": safety_result.checks_passed,
                "checks_failed": safety_result.checks_failed,
                "warnings": safety_result.warnings,
                "provider": safety_result.provider,
            },
            "metadata": metadata or {},
            "recommendations": [],
        }

        # Add recommendations based on findings
        if not safety_result.safe:
            report["recommendations"].append(
                "Payload contains potentially unsafe content"
            )
            report["recommendations"].append("Review payload before further processing")

        if "sensitive_patterns_detected" in safety_result.checks_failed:
            report["recommendations"].append("Remove or mask sensitive data patterns")

        if "pii_entities_detected" in safety_result.checks_failed:
            report["recommendations"].append("Apply PII redaction before storage")

        if safety_result.confidence_score < 0.5:
            report["recommendations"].append(
                "Low confidence in safety assessment - manual review recommended"
            )

        return report


if __name__ == "__main__":
    checker = PayloadSafetyChecker()

    # Test with safe text
    safe_text = "This is a normal business document about quarterly reports."
    safe_result = checker.check_payload_safety(safe_text, use_comprehend=False)
    print(f"Safe text result: {safe_result}")

    # Test with potentially unsafe text
    unsafe_text = "SSN: 123-45-6789, Credit card: 4111-1111-1111-1111, discussing exploit techniques."
    unsafe_result = checker.check_payload_safety(unsafe_text, use_comprehend=False)
    print(f"\nUnsafe text result: {unsafe_result}")

    # Generate report
    report = checker.generate_safety_report(
        unsafe_text, {"source": "test", "key_id": "alias/test-key"}
    )
    print(f"\nSafety report: {json.dumps(report, indent=2)}")
