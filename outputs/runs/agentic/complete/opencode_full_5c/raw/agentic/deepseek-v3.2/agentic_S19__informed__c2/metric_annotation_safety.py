import os
import requests
import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class MetricAnnotationSafetyChecker:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = key or os.environ.get("AZURE_CONTENT_SAFETY_KEY")

        if not self.endpoint or not self.key:
            raise ValueError(
                "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set"
            )

    def check_annotation_safety(
        self, annotation_text: str, categories: List[str] = None
    ) -> Dict[str, Any]:
        if categories is None:
            categories = ["Hate", "SelfHarm", "Sexual", "Violence"]

        url = f"{self.endpoint}/contentsafety/text:analyze?api-version=2023-10-01"

        headers = {
            "Ocp-Apim-Subscription-Key": self.key,
            "Content-Type": "application/json",
        }

        payload = {
            "text": annotation_text,
            "categories": categories,
            "outputType": "FourSeverityLevels",
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            safety_assessment = {
                "text": annotation_text,
                "checked_at": datetime.utcnow().isoformat(),
                "categories_checked": categories,
                "is_safe": True,
                "blocked": False,
                "category_results": {},
                "provider": "azure_content_safety",
            }

            if "categoriesAnalysis" in result:
                for analysis in result["categoriesAnalysis"]:
                    category = analysis.get("category", "")
                    severity = analysis.get("severity", 0)

                    safety_assessment["category_results"][category] = {
                        "severity": severity,
                        "severity_level": self._get_severity_level(severity),
                    }

                    if severity >= 2:
                        safety_assessment["is_safe"] = False

                    if severity >= 3:
                        safety_assessment["blocked"] = True

            return safety_assessment

        except requests.exceptions.RequestException as e:
            return {
                "text": annotation_text,
                "error": str(e),
                "checked_at": datetime.utcnow().isoformat(),
                "is_safe": False,
                "blocked": True,
                "provider": "azure_content_safety",
            }

    def _get_severity_level(self, severity: int) -> str:
        levels = {0: "Safe", 1: "Low", 2: "Medium", 3: "High"}
        return levels.get(severity, "Unknown")

    def check_batch_annotations(self, annotations: List[str]) -> Dict[str, Any]:
        results = []
        unsafe_count = 0
        blocked_count = 0

        for annotation in annotations:
            result = self.check_annotation_safety(annotation)
            results.append(result)

            if not result.get("is_safe", True):
                unsafe_count += 1

            if result.get("blocked", False):
                blocked_count += 1

        return {
            "batch_results": results,
            "total_checked": len(annotations),
            "unsafe_count": unsafe_count,
            "blocked_count": blocked_count,
            "safe_percentage": (
                (len(annotations) - unsafe_count) / len(annotations) * 100
            )
            if annotations
            else 100,
            "checked_at": datetime.utcnow().isoformat(),
            "provider": "azure_content_safety",
        }

    def get_safety_recommendations(self, safety_result: Dict[str, Any]) -> List[str]:
        recommendations = []

        if not safety_result.get("is_safe", True):
            recommendations.append("Annotation contains potentially unsafe content.")

        category_results = safety_result.get("category_results", {})
        for category, result in category_results.items():
            if result.get("severity", 0) >= 2:
                recommendations.append(
                    f"High severity detected in '{category}' category: {result.get('severity_level')}"
                )

        if safety_result.get("blocked", False):
            recommendations.append("Content should be blocked from display.")

        if not recommendations:
            recommendations.append("Content appears safe for display.")

        return recommendations


if __name__ == "__main__":
    checker = MetricAnnotationSafetyChecker()

    test_annotations = [
        "CPU utilization is high on server-01",
        "This is a normal operational metric",
        "User reported issue with performance degradation",
    ]

    for annotation in test_annotations:
        result = checker.check_annotation_safety(annotation)
        print(f"Annotation: {annotation[:50]}...")
        print(f"  Safe: {result.get('is_safe')}")
        print(f"  Blocked: {result.get('blocked')}")
        print()
