import os
import requests
import json
from typing import Dict, List, Any, Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


class MetricAnnotationSafety:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        self.endpoint = endpoint or os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = key or os.getenv("AZURE_CONTENT_SAFETY_KEY")

        if not self.endpoint or not self.key:
            raise ValueError(
                "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set"
            )

        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))

    def check_annotation_safety(
        self, text: str, categories: List[TextCategory] = None
    ) -> Dict[str, Any]:
        try:
            if categories is None:
                categories = [
                    TextCategory.HATE,
                    TextCategory.SELF_HARM,
                    TextCategory.SEXUAL,
                    TextCategory.VIOLENCE,
                ]

            request = AnalyzeTextOptions(text=text, categories=categories)
            response = self.client.analyze_text(request)

            result = {
                "text": text,
                "safe": True,
                "category_results": {},
                "has_issues": False,
            }

            for category_result in response.categories_analysis:
                category_name = category_result.category.name
                severity = category_result.severity

                result["category_results"][category_name] = {
                    "severity": severity,
                    "safe": severity == 0,
                }

                if severity > 0:
                    result["has_issues"] = True
                    result["safe"] = False

            return result

        except HttpResponseError as e:
            print(f"Azure AI Content Safety API error: {e}")
            raise
        except Exception as e:
            print(f"Error checking annotation safety: {e}")
            raise

    def check_multiple_annotations(
        self, annotations: List[str]
    ) -> List[Dict[str, Any]]:
        results = []
        for annotation in annotations:
            result = self.check_annotation_safety(annotation)
            results.append(result)
        return results

    def validate_metric_label(self, label: str, max_severity: int = 1) -> bool:
        result = self.check_annotation_safety(label)

        if not result["safe"]:
            for category_result in result["category_results"].values():
                if category_result["severity"] > max_severity:
                    return False
        return True

    def check_dashboard_notes(self, notes: str) -> Dict[str, Any]:
        return self.check_annotation_safety(notes)

    def filter_unsafe_annotations(self, annotations: List[str]) -> Dict[str, Any]:
        safe_annotations = []
        unsafe_annotations = []

        for annotation in annotations:
            result = self.check_annotation_safety(annotation)
            if result["safe"]:
                safe_annotations.append(annotation)
            else:
                unsafe_annotations.append(
                    {"text": annotation, "issues": result["category_results"]}
                )

        return {
            "total": len(annotations),
            "safe_count": len(safe_annotations),
            "unsafe_count": len(unsafe_annotations),
            "safe_annotations": safe_annotations,
            "unsafe_annotations": unsafe_annotations,
        }


def check_metric_annotation_safety(annotation_text: str) -> Dict[str, Any]:
    checker = MetricAnnotationSafety()
    return checker.check_annotation_safety(annotation_text)


def validate_metric_labels(labels: List[str]) -> Dict[str, Any]:
    checker = MetricAnnotationSafety()
    results = checker.check_multiple_annotations(labels)

    valid_labels = []
    invalid_labels = []

    for i, result in enumerate(results):
        if result["safe"]:
            valid_labels.append(labels[i])
        else:
            invalid_labels.append(
                {"label": labels[i], "issues": result["category_results"]}
            )

    return {
        "total_labels": len(labels),
        "valid_labels": valid_labels,
        "invalid_labels": invalid_labels,
        "valid_count": len(valid_labels),
        "invalid_count": len(invalid_labels),
    }


def check_dashboard_content_safety(dashboard_data: Dict[str, Any]) -> Dict[str, Any]:
    checker = MetricAnnotationSafety()

    checks = {}

    if "title" in dashboard_data:
        checks["title"] = checker.check_annotation_safety(dashboard_data["title"])

    if "description" in dashboard_data:
        checks["description"] = checker.check_annotation_safety(
            dashboard_data["description"]
        )

    if "panels" in dashboard_data:
        panel_checks = []
        for panel in dashboard_data["panels"]:
            panel_check = {}
            if "title" in panel:
                panel_check["title"] = checker.check_annotation_safety(panel["title"])
            if "description" in panel:
                panel_check["description"] = checker.check_annotation_safety(
                    panel["description"]
                )
            panel_checks.append(panel_check)
        checks["panels"] = panel_checks

    all_safe = all(
        check.get("safe", True) for check in checks.values() if isinstance(check, dict)
    )

    return {"dashboard_safe": all_safe, "checks": checks, "has_issues": not all_safe}


def sanitize_metric_annotation(annotation: str) -> Dict[str, Any]:
    checker = MetricAnnotationSafety()
    result = checker.check_annotation_safety(annotation)

    if result["safe"]:
        return {
            "original": annotation,
            "sanitized": annotation,
            "was_modified": False,
            "issues": None,
        }
    else:
        sanitized = _apply_basic_sanitization(annotation)
        sanitized_result = checker.check_annotation_safety(sanitized)

        return {
            "original": annotation,
            "sanitized": sanitized,
            "was_modified": True,
            "original_issues": result["category_results"],
            "sanitized_issues": sanitized_result["category_results"],
            "sanitized_safe": sanitized_result["safe"],
        }


def _apply_basic_sanitization(text: str) -> str:
    offensive_terms = [
        "hate",
        "violence",
        "sexual",
        "harm",
        "attack",
        "kill",
        "hurt",
        "abuse",
        "threat",
        "danger",
    ]

    sanitized = text
    for term in offensive_terms:
        sanitized = sanitized.replace(term, "[REDACTED]")

    return sanitized


def batch_check_metric_annotations(
    annotations: List[Dict[str, str]],
) -> List[Dict[str, Any]]:
    checker = MetricAnnotationSafety()

    results = []
    for annotation_data in annotations:
        annotation_id = annotation_data.get("id", "unknown")
        text = annotation_data.get("text", "")

        safety_result = checker.check_annotation_safety(text)

        results.append(
            {
                "id": annotation_id,
                "text": text,
                "safety_result": safety_result,
                "safe_for_dashboard": safety_result["safe"],
            }
        )

    return results
