"""
record_text_safety.py - Check user-generated document fields for unsafe content
using the OpenAI Moderation API (text-moderation-latest model).
"""

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from database_client import build_atlas_client, AtlasClientHelper
from database_models import (
    DocumentResponse,
    extract_user_text_fields,
    QueryResponse,
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = "text-moderation-latest"


class SafetyCheckResult:
    """Holds the safety check result for a single text field."""

    def __init__(self, field_name: str, text: str, flagged: bool, categories: Dict[str, bool]):
        self.field_name = field_name
        self.text = text
        self.flagged = flagged
        self.categories = categories

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field_name": self.field_name,
            "flagged": self.flagged,
            "categories": self.categories,
            "text_preview": self.text[:100] + ("..." if len(self.text) > 100 else ""),
        }


class DocumentSafetyReport:
    """Aggregated safety report for all user-generated text in a document."""

    def __init__(self, doc_id: str, checks: List[SafetyCheckResult]):
        self.doc_id = doc_id
        self.checks = checks
        self.overall_flagged = any(c.flagged for c in checks)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "overall_flagged": self.overall_flagged,
            "checks": [c.to_dict() for c in self.checks],
            "total_fields_checked": len(self.checks),
            "flagged_fields": sum(1 for c in self.checks if c.flagged),
        }


def check_text_safety(
    text: str,
    client: Optional[OpenAI] = None,
) -> SafetyCheckResult:
    """
    Check a single text string using the OpenAI Moderation API.

    Args:
        text: The text content to evaluate.
        client: Optional pre-configured OpenAI client.

    Returns:
        SafetyCheckResult with flagging details.
    """
    if client is None:
        client = OpenAI(api_key=OPENAI_API_KEY)

    if not text or len(text.strip()) < 2:
        return SafetyCheckResult(
            field_name="",
            text=text,
            flagged=False,
            categories={},
        )

    moderation = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )

    result = moderation.results[0]
    categories = {
        cat: getattr(result.categories, cat, False)
        for cat in dir(result.categories)
        if not cat.startswith("_") and isinstance(getattr(result.categories, cat, None), bool)
    }

    return SafetyCheckResult(
        field_name="input",
        text=text,
        flagged=result.flagged,
        categories=categories,
    )


def check_document_safety(
    doc_response: DocumentResponse,
    client: Optional[OpenAI] = None,
) -> DocumentSafetyReport:
    """
    Check all user-generated text fields in a document for unsafe content.

    Args:
        doc_response: The document to check.
        client: Optional pre-configured OpenAI client.

    Returns:
        DocumentSafetyReport with per-field safety results.
    """
    text_fields = extract_user_text_fields(doc_response.data)
    checks = []

    for field_name, text in text_fields.items():
        result = check_text_safety(text, client=client)
        result.field_name = field_name
        checks.append(result)

    return DocumentSafetyReport(doc_id=doc_response.doc_id, checks=checks)


def check_collection_safety(
    collection_name: str,
    filter_field: Optional[str] = None,
    filter_value: Optional[Any] = None,
    limit: int = 50,
    openai_client: Optional[OpenAI] = None,
    mongo_client: Optional[AtlasClientHelper] = None,
) -> List[DocumentSafetyReport]:
    """
    Fetch documents from MongoDB Atlas and run safety checks on user text fields.

    Args:
        collection_name: MongoDB Atlas collection to query.
        filter_field: Optional field to filter documents by.
        filter_value: Optional value for the filter field.
        limit: Maximum documents to process.
        openai_client: Optional pre-configured OpenAI client.
        mongo_client: Optional pre-built AtlasClientHelper instance.

    Returns:
        List of DocumentSafetyReport objects.
    """
    if mongo_client is None:
        mongo_client = build_atlas_client()

    collection = mongo_client.get_collection(collection_name)

    query = {}
    if filter_field and filter_value is not None:
        query[filter_field] = filter_value

    cursor = collection.find(query).limit(limit)

    reports = []
    for raw_doc in cursor:
        doc_id = str(raw_doc.get("_id", ""))
        data = raw_doc.get("data", {})
        doc_resp = DocumentResponse(doc_id=doc_id, data=data)
        report = check_document_safety(doc_resp, client=openai_client)
        reports.append(report)

    return reports


if __name__ == "__main__":
    reports = check_collection_safety(collection_name="documents", limit=10)
    for r in reports:
        print(r.to_dict())
