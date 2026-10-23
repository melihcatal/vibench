"""
Check user-generated document fields for unsafe content using the OpenAI Moderation API.
Uses the official openai Python SDK with the text-moderation-latest model.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from database_models import DocumentResponse


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "text-moderation-latest"


def check_text_safety(
    text: str,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Evaluate a single text string against OpenAI's moderation model.

    Args:
        text: The text content to analyze.
        client: Optional pre-configured OpenAI client instance.

    Returns:
        Dict with flagged status, category scores, and model info.
    """
    if client is None:
        api_key = os.environ.get(OPENAI_API_KEY_ENV)
        if not api_key:
            raise EnvironmentError(f"Missing environment variable: {OPENAI_API_KEY_ENV}")
        client = OpenAI(api_key=api_key)

    result = client.moderations.create(
        input=text,
        model=OPENAI_MODERATION_MODEL,
    )

    moderation = result.results[0]

    return {
        "flagged": moderation.flagged,
        "categories": dict(moderation.categories),
        "category_scores": dict(moderation.category_scores),
        "model_used": OPENAI_MODERATION_MODEL,
    }


def check_document_safety(
    document: DocumentResponse,
    fields_to_check: Optional[List[str]] = None,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Check user-generated fields within a document for unsafe content
    using OpenAI's text-moderation-latest model.

    Args:
        document: The DocumentResponse to audit.
        fields_to_check: Optional list of specific field names to check.
                         If None, checks all string-valued top-level fields.
        client: Optional pre-configured OpenAI client.

    Returns:
        Dict with overall safety assessment and per-field results.
    """
    data = document.data

    if fields_to_check is None:
        target_fields = [
            k for k, v in data.items() if isinstance(v, str)
        ]
    else:
        target_fields = [k for k in fields_to_check if k in data]

    field_results = {}
    overall_flagged = False

    for field_name in target_fields:
        text_value = data[field_name]
        if isinstance(text_value, str) and text_value.strip():
            safety = check_text_safety(text_value, client=client)
            field_results[field_name] = safety
            if safety["flagged"]:
                overall_flagged = True

    return {
        "document_id": document.id,
        "overall_flagged": overall_flagged,
        "fields_checked": target_fields,
        "field_results": field_results,
        "model_used": OPENAI_MODERATION_MODEL,
    }


def batch_check_document_safety(
    documents: List[DocumentResponse],
    fields_to_check: Optional[List[str]] = None,
    client: Optional[OpenAI] = None,
) -> List[Dict[str, Any]]:
    """
    Run safety checks across a list of documents using OpenAI moderation.

    Args:
        documents: List of DocumentResponse objects.
        fields_to_check: Optional list of field names per document.
        client: Optional pre-configured OpenAI client.

    Returns:
        List of safety assessment dicts, one per document.
    """
    results = []
    for doc in documents:
        safety = check_document_safety(
            document=doc,
            fields_to_check=fields_to_check,
            client=client,
        )
        results.append(safety)
    return results


if __name__ == "__main__":
    import json

    sample_doc = DocumentResponse(
        id="doc-user-42",
        data={
            "title": "User Comment",
            "body": "This is a normal and friendly comment.",
            "author": "alice",
        },
    )
    result = check_document_safety(
        sample_doc,
        fields_to_check=["body"],
    )
    print(json.dumps(result, indent=2))
