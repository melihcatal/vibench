import os
import json
from typing import Dict, Any, List, Optional
import requests


class ContentSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def check_text_safety(
        self, text: str, languages: List[str] = None
    ) -> Dict[str, Any]:
        """
        Check text for unsafe content using Perspective API.

        Args:
            text: Text to analyze
            languages: List of language codes (default: ['en'])

        Returns:
            Safety analysis results
        """
        if languages is None:
            languages = ["en"]

        payload = {
            "comment": {"text": text, "type": "PLAIN_TEXT"},
            "languages": languages,
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {},
                "PROFANITY": {},
                "THREAT": {},
                "SEXUALLY_EXPLICIT": {},
                "FLIRTATION": {},
            },
            "doNotStore": True,
        }

        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()

            result = response.json()
            return self._parse_perspective_response(result)

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to check content safety: {str(e)}") from e

    def check_decrypted_payload(self, decrypted_text: str) -> Dict[str, Any]:
        """
        Check decrypted text payload for unsafe content.

        Args:
            decrypted_text: Decrypted text to analyze

        Returns:
            Safety analysis with recommendations
        """
        safety_result = self.check_text_safety(decrypted_text)

        analysis = {
            "is_safe": True,
            "risk_level": "low",
            "flagged_attributes": [],
            "recommendations": [],
        }

        attribute_scores = safety_result.get("attributeScores", {})

        for attr_name, attr_data in attribute_scores.items():
            score = attr_data.get("summaryScore", {}).get("value", 0)

            if score > 0.7:
                analysis["is_safe"] = False
                analysis["risk_level"] = "high"
                analysis["flagged_attributes"].append(
                    {"attribute": attr_name, "score": score, "threshold": 0.7}
                )
            elif score > 0.4:
                if analysis["risk_level"] == "low":
                    analysis["risk_level"] = "medium"
                analysis["flagged_attributes"].append(
                    {"attribute": attr_name, "score": score, "threshold": 0.4}
                )

        if not analysis["is_safe"]:
            analysis["recommendations"].append(
                "Content contains potentially harmful material"
            )
            analysis["recommendations"].append(
                "Consider redacting or filtering this content"
            )

        if analysis["risk_level"] == "medium":
            analysis["recommendations"].append(
                "Content shows moderate risk - review recommended"
            )

        analysis["overall_score"] = safety_result.get("overallScore", 0)

        return analysis

    def batch_check_safety(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        Check multiple text payloads for safety.

        Args:
            texts: List of texts to analyze

        Returns:
            List of safety analysis results
        """
        results = []
        for text in texts:
            try:
                result = self.check_decrypted_payload(text)
                results.append(result)
            except Exception as e:
                results.append(
                    {"error": str(e), "is_safe": False, "risk_level": "unknown"}
                )

        return results

    def get_safety_summary(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary of safety analysis results.

        Args:
            analyses: List of safety analysis results

        Returns:
            Summary statistics
        """
        total = len(analyses)
        safe_count = sum(1 for a in analyses if a.get("is_safe", False))
        high_risk_count = sum(1 for a in analyses if a.get("risk_level") == "high")
        medium_risk_count = sum(1 for a in analyses if a.get("risk_level") == "medium")

        flagged_attributes = {}
        for analysis in analyses:
            for flagged in analysis.get("flagged_attributes", []):
                attr = flagged.get("attribute")
                if attr:
                    flagged_attributes[attr] = flagged_attributes.get(attr, 0) + 1

        return {
            "total_payloads": total,
            "safe_payloads": safe_count,
            "unsafe_payloads": total - safe_count,
            "high_risk_payloads": high_risk_count,
            "medium_risk_payloads": medium_risk_count,
            "most_common_issues": sorted(
                flagged_attributes.items(), key=lambda x: x[1], reverse=True
            )[:5],
        }

    def _parse_perspective_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Perspective API response."""
        result = {
            "attributeScores": {},
            "overallScore": 0,
            "detectedLanguages": response.get("detectedLanguages", []),
        }

        attribute_scores = response.get("attributeScores", {})
        max_score = 0

        for attr_name, attr_data in attribute_scores.items():
            summary_score = attr_data.get("summaryScore", {})
            score_value = summary_score.get("value", 0)

            result["attributeScores"][attr_name] = {
                "score": score_value,
                "type": summary_score.get("type", "UNKNOWN"),
            }

            if score_value > max_score:
                max_score = score_value

        result["overallScore"] = max_score
        return result


def check_payload_safety(decrypted_text: str) -> Dict[str, Any]:
    """
    Convenience function to check decrypted payload safety.

    Args:
        decrypted_text: Decrypted text to analyze

    Returns:
        Safety analysis results
    """
    checker = ContentSafetyChecker()
    return checker.check_decrypted_payload(decrypted_text)
