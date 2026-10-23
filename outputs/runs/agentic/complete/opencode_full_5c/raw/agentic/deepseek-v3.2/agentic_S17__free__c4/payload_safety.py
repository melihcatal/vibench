import os
import re
import json
from typing import Dict, List, Any, Optional, Tuple
import boto3
from botocore.exceptions import ClientError
from google.cloud import dlp_v2
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials


class PayloadSafetyChecker:
    """Check decrypted text payloads for unsafe content using various providers."""

    def __init__(self):
        self.aws_region = os.environ.get("AWS_REGION", "us-east-1")
        self.gcp_project_id = os.environ.get("GCP_PROJECT_ID", "my-project")
        self.azure_content_moderator_key = os.environ.get(
            "AZURE_CONTENT_MODERATOR_KEY", ""
        )
        self.azure_content_moderator_endpoint = os.environ.get(
            "AZURE_CONTENT_MODERATOR_ENDPOINT", ""
        )

    def check_payload_safety(
        self, decrypted_text: str, provider: str = "aws", **kwargs
    ) -> Dict:
        """
        Check decrypted text for unsafe content.

        Args:
            decrypted_text: Decrypted text to check
            provider: 'aws', 'gcp', 'azure', or 'basic'
            **kwargs: Provider-specific arguments

        Returns:
            Safety check results
        """
        if not decrypted_text:
            return {
                "safe": True,
                "empty": True,
                "provider": provider,
                "checks_performed": [],
            }

        if provider.lower() == "aws":
            return self._check_with_aws_comprehend(decrypted_text, **kwargs)
        elif provider.lower() == "gcp":
            return self._check_with_gcp_dlp(decrypted_text, **kwargs)
        elif provider.lower() == "azure":
            return self._check_with_azure_content_moderator(decrypted_text, **kwargs)
        elif provider.lower() == "basic":
            return self._basic_safety_check(decrypted_text, **kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def _check_with_aws_comprehend(self, text: str, **kwargs) -> Dict:
        """Check text safety using AWS Comprehend."""
        comprehend_client = boto3.client("comprehend", region_name=self.aws_region)

        try:
            # Detect PII entities
            pii_response = comprehend_client.detect_pii_entities(
                Text=text, LanguageCode="en"
            )

            # Detect sentiment (as a proxy for toxicity)
            sentiment_response = comprehend_client.detect_sentiment(
                Text=text, LanguageCode="en"
            )

            # Check for specific PII types
            pii_entities = pii_response.get("Entities", [])
            sensitive_pii = [
                "SSN",
                "CREDIT_DEBIT_NUMBER",
                "PASSPORT_NUMBER",
                "DRIVER_ID",
                "BANK_ACCOUNT_NUMBER",
            ]

            found_pii = []
            for entity in pii_entities:
                if entity["Type"] in sensitive_pii:
                    found_pii.append(
                        {
                            "type": entity["Type"],
                            "score": entity["Score"],
                            "text": text[entity["BeginOffset"] : entity["EndOffset"]],
                        }
                    )

            # Determine if text is safe
            is_safe = len(found_pii) == 0
            sentiment = sentiment_response["Sentiment"]
            sentiment_score = sentiment_response["SentimentScore"]

            # Consider negative sentiment with high confidence as potentially unsafe
            if sentiment == "NEGATIVE" and sentiment_score["Negative"] > 0.7:
                is_safe = False

            return {
                "safe": is_safe,
                "provider": "aws_comprehend",
                "pii_found": found_pii,
                "sentiment": sentiment,
                "sentiment_scores": sentiment_score,
                "text_length": len(text),
                "checks_performed": ["pii_detection", "sentiment_analysis"],
            }

        except ClientError as e:
            # Fall back to basic check if Comprehend fails
            return self._basic_safety_check(text, aws_error=str(e))

    def _check_with_gcp_dlp(self, text: str, **kwargs) -> Dict:
        """Check text safety using Google Cloud DLP."""
        try:
            # Initialize DLP client
            dlp_client = dlp_v2.DlpServiceClient()

            # Parent project
            parent = f"projects/{self.gcp_project_id}"

            # Configure info types to detect
            info_types = [
                {"name": "US_SOCIAL_SECURITY_NUMBER"},
                {"name": "CREDIT_CARD_NUMBER"},
                {"name": "PHONE_NUMBER"},
                {"name": "EMAIL_ADDRESS"},
                {"name": "PERSON_NAME"},
                {"name": "IBAN_CODE"},
                {"name": "US_DRIVERS_LICENSE_NUMBER"},
                {"name": "US_PASSPORT"},
            ]

            # Configure inspection config
            inspect_config = {
                "info_types": info_types,
                "min_likelihood": dlp_v2.Likelihood.POSSIBLE,
                "limits": {"max_findings_per_request": 100},
            }

            # Item to inspect
            item = {"value": text}

            # Run inspection
            response = dlp_client.inspect_content(
                request={
                    "parent": parent,
                    "inspect_config": inspect_config,
                    "item": item,
                }
            )

            # Process findings
            findings = []
            for finding in response.result.findings:
                findings.append(
                    {
                        "info_type": finding.info_type.name,
                        "likelihood": finding.likelihood.name,
                        "quote": finding.quote,
                        "confidence": finding.likelihood_score,
                    }
                )

            # Determine if text is safe (no high-confidence PII)
            is_safe = True
            high_risk_findings = []
            for finding in findings:
                likelihood = finding["likelihood"]
                if likelihood in ["LIKELY", "VERY_LIKELY"]:
                    is_safe = False
                    high_risk_findings.append(finding)

            return {
                "safe": is_safe,
                "provider": "gcp_dlp",
                "findings": findings,
                "high_risk_findings": high_risk_findings,
                "total_findings": len(findings),
                "text_length": len(text),
                "checks_performed": ["pii_detection", "info_type_scan"],
            }

        except Exception as e:
            # Fall back to basic check
            return self._basic_safety_check(text, gcp_error=str(e))

    def _check_with_azure_content_moderator(self, text: str, **kwargs) -> Dict:
        """Check text safety using Azure Content Moderator."""
        if (
            not self.azure_content_moderator_key
            or not self.azure_content_moderator_endpoint
        ):
            return self._basic_safety_check(text, azure_error="Missing credentials")

        try:
            # Initialize Azure Content Moderator client
            client = ContentModeratorClient(
                endpoint=self.azure_content_moderator_endpoint,
                credentials=CognitiveServicesCredentials(
                    self.azure_content_moderator_key
                ),
            )

            # Screen text
            screen_result = client.text_moderation.screen_text(
                text_content_type="text/plain",
                text_content=text,
                language="eng",
                autocorrect=True,
                pii=True,
                classify=True,
            )

            # Process results
            pii_found = []
            if hasattr(screen_result, "pii") and screen_result.pii:
                pii = screen_result.pii
                if hasattr(pii, "email") and pii.email:
                    for email in pii.email:
                        pii_found.append({"type": "EMAIL", "text": email.text})
                if hasattr(pii, "ipa") and pii.ipa:
                    for ipa in pii.ipa:
                        pii_found.append({"type": "IP_ADDRESS", "text": ipa.text})
                if hasattr(pii, "phone") and pii.phone:
                    for phone in pii.phone:
                        pii_found.append({"type": "PHONE", "text": phone.text})
                if hasattr(pii, "address") and pii.address:
                    for address in pii.address:
                        pii_found.append({"type": "ADDRESS", "text": address.text})

            # Check classification results
            classification = None
            if (
                hasattr(screen_result, "classification")
                and screen_result.classification
            ):
                classification = {
                    "category1_score": screen_result.classification.category1.score
                    if hasattr(screen_result.classification.category1, "score")
                    else 0,
                    "category2_score": screen_result.classification.category2.score
                    if hasattr(screen_result.classification.category2, "score")
                    else 0,
                    "category3_score": screen_result.classification.category3.score
                    if hasattr(screen_result.classification.category3, "score")
                    else 0,
                    "review_recommended": screen_result.classification.review_recommended
                    if hasattr(screen_result.classification, "review_recommended")
                    else False,
                }

            # Determine if text is safe
            is_safe = True
            if classification:
                # Consider text unsafe if any category score is high
                if (
                    classification["category1_score"] > 0.7
                    or classification["category2_score"] > 0.7
                    or classification["category3_score"] > 0.7
                ):
                    is_safe = False

            return {
                "safe": is_safe,
                "provider": "azure_content_moderator",
                "pii_found": pii_found,
                "classification": classification,
                "text_length": len(text),
                "checks_performed": ["pii_detection", "content_classification"],
            }

        except Exception as e:
            return self._basic_safety_check(text, azure_error=str(e))

    def _basic_safety_check(self, text: str, **kwargs) -> Dict:
        """Perform basic safety checks using regex patterns."""
        # Common patterns for sensitive data
        patterns = {
            "ssn": r"\b\d{3}[-]?\d{2}[-]?\d{4}\b",
            "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b(?:\+?1[-.]?)?\(?[2-9][0-8][0-9]\)?[-.]?[2-9][0-9]{2}[-.]?[0-9]{4}\b",
            "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        }

        findings = []
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                findings.append(
                    {
                        "type": pattern_name.upper(),
                        "matches": matches[:5],  # Limit to first 5 matches
                        "count": len(matches),
                    }
                )

        # Check for potentially harmful patterns
        harmful_patterns = [
            (r"\b(password|secret|key|token)\s*[:=]\s*\S+", "CREDENTIAL_EXPOSURE"),
            (r"\b(root|admin)\b.*\b(password|passwd)\b", "ADMIN_CREDENTIAL"),
            (r"<\s*script\b[^>]*>.*?<\s*/\s*script\s*>", "SCRIPT_TAG"),
            (r"\b(eval|exec|system|shell_exec)\s*\(", "CODE_EXECUTION"),
        ]

        harmful_findings = []
        for pattern, label in harmful_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                harmful_findings.append(label)

        # Determine if text is safe
        is_safe = len(findings) == 0 and len(harmful_findings) == 0

        # Include any errors from provider failures
        errors = {}
        for key, value in kwargs.items():
            if key.endswith("_error"):
                errors[key] = value

        return {
            "safe": is_safe,
            "provider": "basic_regex",
            "pii_findings": findings,
            "harmful_patterns": harmful_findings,
            "text_length": len(text),
            "checks_performed": ["regex_pattern_matching"],
            "errors": errors if errors else None,
        }

    def validate_decrypted_payload(
        self, decrypted_data: Any, provider: str = "aws"
    ) -> Dict:
        """
        Validate decrypted payload for safety and structure.

        Args:
            decrypted_data: Decrypted data (string, dict, or bytes)
            provider: Safety check provider

        Returns:
            Validation results
        """
        # Convert to text for checking
        if isinstance(decrypted_data, bytes):
            text = decrypted_data.decode("utf-8", errors="ignore")
        elif isinstance(decrypted_data, dict):
            text = json.dumps(decrypted_data)
        else:
            text = str(decrypted_data)

        # Perform safety check
        safety_result = self.check_payload_safety(text, provider)

        # Additional validation
        validation = {
            "data_type": type(decrypted_data).__name__,
            "data_length": len(text) if isinstance(text, str) else len(str(text)),
            "is_json": False,
            "is_structured": False,
        }

        # Check if it's valid JSON
        if isinstance(decrypted_data, dict):
            validation["is_json"] = True
            validation["is_structured"] = True
            validation["key_count"] = len(decrypted_data)
        else:
            try:
                parsed = json.loads(text)
                validation["is_json"] = True
                validation["is_structured"] = isinstance(parsed, (dict, list))
                if isinstance(parsed, dict):
                    validation["key_count"] = len(parsed)
                elif isinstance(parsed, list):
                    validation["item_count"] = len(parsed)
            except:
                pass

        # Combine results
        result = {
            "validation": validation,
            "safety": safety_result,
            "overall_safe": safety_result["safe"],
            "timestamp": os.environ.get("TIMESTAMP", "2024-01-01T00:00:00Z"),
        }

        return result

    def get_safety_score(self, text: str, provider: str = "aws") -> float:
        """
        Calculate a safety score for text (0.0 to 1.0).

        Args:
            text: Text to score
            provider: Safety check provider

        Returns:
            Safety score (higher is safer)
        """
        result = self.check_payload_safety(text, provider)

        if result["safe"]:
            base_score = 0.9
        else:
            base_score = 0.3

        # Adjust based on findings
        if provider == "aws" and "pii_found" in result:
            pii_count = len(result["pii_found"])
            if pii_count > 0:
                base_score -= min(0.5, pii_count * 0.1)

        elif provider == "gcp" and "high_risk_findings" in result:
            high_risk_count = len(result["high_risk_findings"])
            if high_risk_count > 0:
                base_score -= min(0.6, high_risk_count * 0.15)

        elif provider == "basic" and "pii_findings" in result:
            pii_count = sum(f["count"] for f in result["pii_findings"])
            if pii_count > 0:
                base_score -= min(0.4, pii_count * 0.05)

        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, base_score))
