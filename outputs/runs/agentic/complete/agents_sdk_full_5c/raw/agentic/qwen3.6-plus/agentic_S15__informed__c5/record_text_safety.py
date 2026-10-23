"""
Check user-generated document fields for unsafe content using Azure AI Content Safety.

Uses the azure-ai-contentsafety SDK to analyze text for hate speech, self-harm,
sexual content, and violence categories. Requires AZURE_CONTENT_SAFETY_ENDPOINT
and AZURE_CONTENT_SAFETY_KEY environment variables.
"""

import json
import os
import sys
from typing import Any, Dict, List, Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

from database_models import extract_text_fields


def check_text_safety(
    document: Dict[str, Any],
    text_fields: Optional[List[str]] = None,
    hate_threshold: int = 4,
    self_harm_threshold: int = 4,
    sexual_threshold: int = 4,
    violence_threshold: int = 4,
) -> Dict[str, Any]:
    """Check document text fields for unsafe content using Azure AI Content Safety.

    Args:
        document: The document dict containing text fields to analyze.
        text_fields: Specific field names to check. If None, common text fields
                     (title, description, content, body, text, summary, notes) are used.
        hate_threshold: Severity threshold (0-8) for hate content. Default 4.
        self_harm_threshold: Severity threshold for self-harm content. Default 4.
        sexual_threshold: Severity threshold for sexual content. Default 4.
        violence_threshold: Severity threshold for violent content. Default 4.

    Returns:
        Dict with 'success', 'safe', 'results' per field, and optional 'error'.
    """
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not api_key:
        return {
            "success": False,
            "error": (
                "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY "
                "environment variables are required"
            ),
            "safe": None,
            "results": [],
        }

    client = ContentSafetyClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key),
    )

    texts = extract_text_fields(document, text_fields)
    results = []
    overall_safe = True

    for text in texts:
        if not text.strip():
            continue

        field_result = {
            "text_preview": text[:100] + ("..." if len(text) > 100 else ""),
            "safe": True,
            "categories": {},
            "flagged_categories": [],
        }

        try:
            analysis = client.analyze_text(
                text=text,
            )

            if analysis.hate_result:
                field_result["categories"]["hate"] = analysis.hate_result.severity
                if analysis.hate_result.severity >= hate_threshold:
                    field_result["safe"] = False
                    field_result["flagged_categories"].append("hate")

            if analysis.self_harm_result:
                field_result["categories"]["self_harm"] = analysis.self_harm_result.severity
                if analysis.self_harm_result.severity >= self_harm_threshold:
                    field_result["safe"] = False
                    field_result["flagged_categories"].append("self_harm")

            if analysis.sexual_result:
                field_result["categories"]["sexual"] = analysis.sexual_result.severity
                if analysis.sexual_result.severity >= sexual_threshold:
                    field_result["safe"] = False
                    field_result["flagged_categories"].append("sexual")

            if analysis.violence_result:
                field_result["categories"]["violence"] = analysis.violence_result.severity
                if analysis.violence_result.severity >= violence_threshold:
                    field_result["safe"] = False
                    field_result["flagged_categories"].append("violence")

        except HttpResponseError as exc:
            field_result["safe"] = None
            field_result["error"] = str(exc)

        if field_result["safe"] is False:
            overall_safe = False

        results.append(field_result)

    return {
        "success": True,
        "safe": overall_safe,
        "document_id": document.get("doc_id", document.get("document_id")),
        "results": results,
        "thresholds": {
            "hate": hate_threshold,
            "self_harm": self_harm_threshold,
            "sexual": sexual_threshold,
            "violence": violence_threshold,
        },
    }


def check_multiple_documents_safety(
    documents: List[Dict[str, Any]],
    text_fields: Optional[List[str]] = None,
    hate_threshold: int = 4,
    self_harm_threshold: int = 4,
    sexual_threshold: int = 4,
    violence_threshold: int = 4,
) -> Dict[str, Any]:
    """Run safety checks across multiple documents and aggregate results."""
    all_results = []
    any_unsafe = False

    for doc in documents:
        result = check_text_safety(
            document=doc,
            text_fields=text_fields,
            hate_threshold=hate_threshold,
            self_harm_threshold=self_harm_threshold,
            sexual_threshold=sexual_threshold,
            violence_threshold=violence_threshold,
        )
        if result.get("safe") is False:
            any_unsafe = True
        all_results.append(result)

    return {
        "success": all(r.get("success") for r in all_results),
        "overall_safe": not any_unsafe,
        "document_count": len(all_results),
        "results": all_results,
    }


if __name__ == "__main__":
    raw_input = sys.stdin.read() if not sys.stdin.isatty() else ""

    if raw_input:
        data = json.loads(raw_input)
    else:
        data = {
            "document": {
                "doc_id": "doc-001",
                "title": "User Comment",
                "content": "This is a normal user comment with no issues.",
                "author": "user123",
            },
            "text_fields": ["title", "content"],
        }

    if "documents" in data:
        result = check_multiple_documents_safety(
            documents=data["documents"],
            text_fields=data.get("text_fields"),
        )
    else:
        result = check_text_safety(
            document=data.get("document", {}),
            text_fields=data.get("text_fields"),
        )
    print(json.dumps(result, indent=2))
