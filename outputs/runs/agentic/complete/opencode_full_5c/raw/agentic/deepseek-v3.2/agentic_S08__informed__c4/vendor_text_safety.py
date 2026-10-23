import os
import json
from typing import Dict, Any, List, Optional
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def moderate_vendor_notes(
    vendor_notes: str, vendor_name: Optional[str] = None
) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure AI Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    request = AnalyzeTextOptions(text=vendor_notes)

    try:
        response = client.analyze_text(request)

        moderation_results = {
            "vendor_name": vendor_name,
            "text_preview": vendor_notes[:100] + "..."
            if len(vendor_notes) > 100
            else vendor_notes,
            "text_length": len(vendor_notes),
            "categories": {},
            "overall_severity": 0,
            "is_safe": True,
            "provider": "azure_ai_content_safety",
        }

        for category_result in response.categories_analysis:
            category_name = category_result.category.value
            severity = category_result.severity

            moderation_results["categories"][category_name] = {
                "severity": severity,
                "severity_level": get_severity_level(severity),
                "threshold_exceeded": severity > 0,
            }

            if severity > moderation_results["overall_severity"]:
                moderation_results["overall_severity"] = severity

            if severity > 0:
                moderation_results["is_safe"] = False

        moderation_results["severity_level"] = get_severity_level(
            moderation_results["overall_severity"]
        )

        return moderation_results

    except Exception as e:
        return {
            "error": str(e),
            "vendor_name": vendor_name,
            "text_preview": vendor_notes[:100] + "..."
            if len(vendor_notes) > 100
            else vendor_notes,
            "provider": "azure_ai_content_safety",
            "analysis_failed": True,
        }


def get_severity_level(severity: int) -> str:
    if severity == 0:
        return "safe"
    elif severity == 2:
        return "low"
    elif severity == 4:
        return "medium"
    elif severity == 6:
        return "high"
    else:
        return "unknown"


def moderate_vendor_fields(vendor_data: Dict[str, Any]) -> Dict[str, Any]:
    moderation_results = {
        "vendor_name": vendor_data.get("vendor_name"),
        "fields_analyzed": [],
        "unsafe_fields": [],
        "overall_assessment": "safe",
        "detailed_results": {},
    }

    fields_to_check = [
        ("vendor_name", vendor_data.get("vendor_name")),
        ("description", vendor_data.get("description")),
        ("notes", vendor_data.get("notes")),
        ("memo", vendor_data.get("memo")),
        ("address", vendor_data.get("address")),
    ]

    for field_name, field_value in fields_to_check:
        if field_value and isinstance(field_value, str):
            result = moderate_vendor_notes(field_value, vendor_data.get("vendor_name"))

            moderation_results["detailed_results"][field_name] = result
            moderation_results["fields_analyzed"].append(field_name)

            if not result.get("is_safe", True):
                moderation_results["unsafe_fields"].append(field_name)
                moderation_results["overall_assessment"] = "unsafe"

    if (
        moderation_results["overall_assessment"] == "safe"
        and moderation_results["fields_analyzed"]
    ):
        max_severity = 0
        for field_name in moderation_results["fields_analyzed"]:
            field_result = moderation_results["detailed_results"][field_name]
            if "overall_severity" in field_result:
                max_severity = max(max_severity, field_result["overall_severity"])

        if max_severity > 0:
            moderation_results["overall_assessment"] = get_severity_level(max_severity)

    return moderation_results


def batch_moderate_vendors(vendors_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    batch_results = {
        "total_vendors": len(vendors_data),
        "safe_vendors": 0,
        "unsafe_vendors": 0,
        "vendors_requiring_review": [],
        "summary_by_severity": {"safe": 0, "low": 0, "medium": 0, "high": 0},
        "detailed_results": {},
    }

    for vendor_data in vendors_data:
        vendor_name = vendor_data.get("vendor_name", "Unknown")
        moderation_result = moderate_vendor_fields(vendor_data)

        batch_results["detailed_results"][vendor_name] = moderation_result

        assessment = moderation_result.get("overall_assessment", "safe")

        if assessment == "safe":
            batch_results["safe_vendors"] += 1
            batch_results["summary_by_severity"]["safe"] += 1
        else:
            batch_results["unsafe_vendors"] += 1

            if assessment in batch_results["summary_by_severity"]:
                batch_results["summary_by_severity"][assessment] += 1

            if assessment in ["medium", "high"]:
                batch_results["vendors_requiring_review"].append(
                    {
                        "vendor_name": vendor_name,
                        "assessment": assessment,
                        "unsafe_fields": moderation_result.get("unsafe_fields", []),
                    }
                )

    return batch_results


def check_vendor_against_blocklist(
    vendor_name: str, blocklist: List[str]
) -> Dict[str, Any]:
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError("Azure AI Content Safety credentials not configured")

    client = ContentSafetyClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    blocklist_check = {
        "vendor_name": vendor_name,
        "in_blocklist": False,
        "blocklist_matches": [],
        "provider": "azure_ai_content_safety",
    }

    for blocked_term in blocklist:
        if blocked_term.lower() in vendor_name.lower():
            blocklist_check["in_blocklist"] = True
            blocklist_check["blocklist_matches"].append(blocked_term)

    if blocklist_check["in_blocklist"]:
        request = AnalyzeTextOptions(text=vendor_name)
        try:
            response = client.analyze_text(request)

            blocklist_check["content_safety_analysis"] = {
                "overall_severity": 0,
                "categories": {},
            }

            for category_result in response.categories_analysis:
                category_name = category_result.category.value
                severity = category_result.severity

                blocklist_check["content_safety_analysis"]["categories"][
                    category_name
                ] = {
                    "severity": severity,
                    "severity_level": get_severity_level(severity),
                }

                if (
                    severity
                    > blocklist_check["content_safety_analysis"]["overall_severity"]
                ):
                    blocklist_check["content_safety_analysis"]["overall_severity"] = (
                        severity
                    )

            blocklist_check["content_safety_analysis"]["severity_level"] = (
                get_severity_level(
                    blocklist_check["content_safety_analysis"]["overall_severity"]
                )
            )

        except Exception as e:
            blocklist_check["content_safety_error"] = str(e)

    return blocklist_check
