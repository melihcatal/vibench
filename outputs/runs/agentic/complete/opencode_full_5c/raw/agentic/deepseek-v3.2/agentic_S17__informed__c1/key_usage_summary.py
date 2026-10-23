import os
import json
from typing import Dict, Any, List, Optional
import anthropic


class KeyUsageAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def summarize_key_usage(self, crypto_events: List[Dict[str, Any]]) -> str:
        """
        Summarize key usage and crypto events using Anthropic Claude.

        Args:
            crypto_events: List of encryption/decryption/signing events

        Returns:
            Summary of key usage patterns
        """
        events_text = self._format_events_for_prompt(crypto_events)

        prompt = f"""You are a security analyst summarizing key management and encryption events.
        
Here are the cryptographic events to analyze:
{events_text}

Please provide a concise summary that includes:
1. Overall usage patterns (encryption vs decryption vs signing)
2. Key rotation and lifecycle observations
3. Any unusual patterns or potential security concerns
4. Recommendations for key management improvements

Focus on actionable insights for security teams."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text

        except Exception as e:
            raise RuntimeError(f"Failed to generate summary: {str(e)}") from e

    def analyze_key_rotation(self, key_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze key rotation patterns and provide recommendations.

        Args:
            key_events: List of key-related events

        Returns:
            Analysis with recommendations
        """
        events_text = self._format_events_for_prompt(key_events)

        prompt = f"""Analyze these key management events for rotation patterns:

{events_text}

Provide analysis in JSON format with these fields:
- "rotation_frequency": estimated rotation frequency
- "keys_at_risk": list of keys that may need rotation
- "recommendations": specific rotation recommendations
- "compliance_notes": any compliance considerations"""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                temperature=0.2,
                messages=[{"role": "user", "content": prompt}],
            )

            analysis_text = response.content[0].text

            try:
                return json.loads(analysis_text)
            except json.JSONDecodeError:
                return {"analysis": analysis_text}

        except Exception as e:
            raise RuntimeError(f"Failed to analyze key rotation: {str(e)}") from e

    def generate_compliance_report(self, audit_trail: List[Dict[str, Any]]) -> str:
        """
        Generate compliance report for crypto operations.

        Args:
            audit_trail: Audit trail of cryptographic operations

        Returns:
            Compliance report
        """
        audit_text = self._format_events_for_prompt(audit_trail)

        prompt = f"""Generate a compliance report for these cryptographic operations:

{audit_text}

Consider:
- Data protection regulations (GDPR, HIPAA, etc.)
- Key management best practices
- Audit trail completeness
- Access control patterns

Provide a structured report suitable for compliance officers."""

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1200,
                temperature=0.1,
                messages=[{"role": "user", "content": prompt}],
            )

            return response.content[0].text

        except Exception as e:
            raise RuntimeError(f"Failed to generate compliance report: {str(e)}") from e

    def _format_events_for_prompt(self, events: List[Dict[str, Any]]) -> str:
        """Format events for LLM prompt."""
        formatted = []
        for i, event in enumerate(events, 1):
            event_str = f"Event {i}:\n"
            for key, value in event.items():
                if key in ["plaintext", "ciphertext", "signature"] and isinstance(
                    value, (bytes, str)
                ):
                    if len(str(value)) > 100:
                        event_str += f"  {key}: [truncated data]\n"
                    else:
                        event_str += f"  {key}: {value}\n"
                else:
                    event_str += f"  {key}: {value}\n"
            formatted.append(event_str)

        return "\n".join(formatted)


def summarize_key_operations(operations: List[Dict[str, Any]]) -> str:
    """
    Convenience function to summarize key operations.

    Args:
        operations: List of cryptographic operations

    Returns:
        Summary text
    """
    analyzer = KeyUsageAnalyzer()
    return analyzer.summarize_key_usage(operations)
