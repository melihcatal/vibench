import os
import re
from typing import List, Dict, Any, Optional
from google.cloud import language_v1


class PayloadSafetyChecker:
    """Check decrypted text payloads for unsafe content using Google Cloud Natural Language API."""

    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

    def check_payload(self, plaintext: str) -> Dict[str, Any]:
        """Analyze plaintext for safety concerns."""

        # Basic pattern matching for sensitive data
        sensitive_patterns = {
            "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
            "ssn": r"\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            "ip_address": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        }

        pattern_matches = {}
        for pattern_name, pattern in sensitive_patterns.items():
            matches = re.findall(pattern, plaintext, re.IGNORECASE)
            if matches:
                pattern_matches[pattern_name] = len(matches)

        # Use Google Cloud Natural Language API for sentiment and entity analysis
        document = language_v1.Document(
            content=plaintext, type_=language_v1.Document.Type.PLAIN_TEXT
        )

        # Analyze sentiment
        sentiment_response = self.client.analyze_sentiment(
            request={"document": document}
        )
        sentiment_score = sentiment_response.document_sentiment.score
        sentiment_magnitude = sentiment_response.document_sentiment.magnitude

        # Analyze entities
        entity_response = self.client.analyze_entities(request={"document": document})

        # Categorize entities
        entity_categories = {}
        sensitive_entities = []

        for entity in entity_response.entities:
            entity_type = language_v1.Entity.Type(entity.type_).name
            if entity_type not in entity_categories:
                entity_categories[entity_type] = 0
            entity_categories[entity_type] += 1

            # Check for potentially sensitive entity types
            if entity_type in [
                "PERSON",
                "LOCATION",
                "ADDRESS",
                "PHONE_NUMBER",
                "EMAIL",
            ]:
                sensitive_entities.append(
                    {
                        "name": entity.name,
                        "type": entity_type,
                        "salience": entity.salience,
                    }
                )

        # Analyze syntax for potential malicious patterns
        syntax_response = self.client.analyze_syntax(request={"document": document})

        # Check for suspicious command patterns
        suspicious_commands = [
            "DROP",
            "DELETE",
            "UPDATE",
            "INSERT",
            "SELECT",
            "rm ",
            "chmod",
            "chown",
            "sudo",
            "curl",
            "wget",
        ]

        command_matches = []
        for token in syntax_response.tokens:
            text = token.text.content.upper()
            for cmd in suspicious_commands:
                if cmd in text:
                    command_matches.append(token.text.content)

        # Determine safety score (0-100, higher is safer)
        safety_score = 100

        # Deduct for pattern matches
        for pattern_name, count in pattern_matches.items():
            safety_score -= count * 5

        # Deduct for sensitive entities
        safety_score -= len(sensitive_entities) * 3

        # Deduct for suspicious commands
        safety_score -= len(command_matches) * 10

        # Adjust for negative sentiment
        if sentiment_score < -0.5:
            safety_score -= 10

        # Ensure score stays within bounds
        safety_score = max(0, min(100, safety_score))

        safety_level = "SAFE"
        if safety_score < 50:
            safety_level = "UNSAFE"
        elif safety_score < 75:
            safety_level = "CAUTION"

        return {
            "provider": "google-cloud-natural-language",
            "safety_score": safety_score,
            "safety_level": safety_level,
            "pattern_analysis": {
                "sensitive_patterns_found": pattern_matches,
                "total_pattern_matches": sum(pattern_matches.values()),
            },
            "entity_analysis": {
                "entity_categories": entity_categories,
                "sensitive_entities": sensitive_entities,
                "total_entities": len(entity_response.entities),
            },
            "sentiment_analysis": {
                "score": sentiment_score,
                "magnitude": sentiment_magnitude,
                "label": "NEGATIVE"
                if sentiment_score < -0.1
                else "POSITIVE"
                if sentiment_score > 0.1
                else "NEUTRAL",
            },
            "security_analysis": {
                "suspicious_commands_found": command_matches,
                "contains_sql_keywords": any(
                    cmd in ["DROP", "DELETE", "UPDATE", "INSERT", "SELECT"]
                    for cmd in command_matches
                ),
            },
            "recommendations": self._generate_recommendations(
                pattern_matches, sensitive_entities, command_matches, safety_level
            ),
        }

    def _generate_recommendations(
        self, pattern_matches, sensitive_entities, command_matches, safety_level
    ):
        """Generate safety recommendations."""
        recommendations = []

        if safety_level == "UNSAFE":
            recommendations.append(
                "Payload contains potentially unsafe content. Review before processing."
            )

        if pattern_matches:
            pattern_list = ", ".join(pattern_matches.keys())
            recommendations.append(
                f"Found sensitive patterns: {pattern_list}. Consider data masking."
            )

        if sensitive_entities:
            recommendations.append(
                f"Found {len(sensitive_entities)} sensitive entities (PII). Ensure proper handling."
            )

        if command_matches:
            recommendations.append(
                "Payload contains suspicious command patterns. Sanitize input."
            )

        if not recommendations:
            recommendations.append("Payload appears safe for processing.")

        return recommendations


def check_payload_safety(plaintext: str) -> Dict[str, Any]:
    """Check decrypted text payloads for unsafe content."""
    checker = PayloadSafetyChecker()
    return checker.check_payload(plaintext)


if __name__ == "__main__":
    # Example usage
    test_payload = "User John Doe with SSN 123-45-6789 requested access. Contact at john@example.com or 555-123-4567."

    safety_result = check_payload_safety(test_payload)
    print(f"Payload safety check: {safety_result}")
