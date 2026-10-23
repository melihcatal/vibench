"""
record_summary.py - Summarize retrieved document records using OpenAI API.
Uses the openai Python SDK to connect to OpenAI's gpt-4o model for generating
intelligent summaries of document content stored in a NoSQL document store.
"""

import os
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI

from database_client import build_atlas_client, AtlasClientHelper
from database_models import (
    DocumentResponse,
    QueryResponse,
    summarize_document_fields,
    extract_user_text_fields,
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL_ID = "gpt-4o"


def summarize_document_text(
    text: str,
    max_words: int = 50,
    client: Optional[OpenAI] = None,
) -> str:
    """
    Summarize a single text field using OpenAI's gpt-4o model.

    Args:
        text: The text content to summarize.
        max_words: Approximate maximum word count for the summary.
        client: Optional pre-configured OpenAI client.

    Returns:
        A concise summary string.
    """
    if not text or len(text.strip()) < 10:
        return text

    if client is None:
        client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=OPENAI_MODEL_ID,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document summarization assistant. "
                    f"Summarize the following text in at most {max_words} words. "
                    "Return only the summary, no additional text."
                ),
            },
            {"role": "user", "content": text},
        ],
        max_tokens=256,
        temperature=0.3,
    )

    summary = response.choices[0].message.content
    return summary.strip() if summary else text


def summarize_record(
    doc_response: DocumentResponse,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Create a structured summary of a single document record.

    Args:
        doc_response: The document to summarize.
        client: Optional pre-configured OpenAI client.

    Returns:
        Dictionary with summary statistics and AI-generated summary.
    """
    data = doc_response.data
    field_summary = summarize_document_fields(data)
    text_fields = extract_user_text_fields(data)

    summaries = {}
    for key, text in text_fields.items():
        summaries[key] = summarize_document_text(text, client=client)

    return {
        "doc_id": doc_response.doc_id,
        "exists": doc_response.exists,
        "field_count": field_summary["field_count"],
        "field_types": field_summary["field_types"],
        "ai_summaries": summaries,
    }


def summarize_records_batch(
    collection_name: str,
    filter_field: Optional[str] = None,
    filter_value: Optional[Any] = None,
    limit: int = 20,
    openai_client: Optional[OpenAI] = None,
    mongo_client: Optional[AtlasClientHelper] = None,
) -> List[Dict[str, Any]]:
    """
    Fetch documents from MongoDB Atlas and generate summaries for each.

    Args:
        collection_name: MongoDB Atlas collection to query.
        filter_field: Optional field to filter documents by.
        filter_value: Optional value for the filter field.
        limit: Maximum documents to process.
        openai_client: Optional pre-configured OpenAI client.
        mongo_client: Optional pre-built AtlasClientHelper instance.

    Returns:
        List of summary dictionaries, one per document.
    """
    if mongo_client is None:
        mongo_client = build_atlas_client()

    collection = mongo_client.get_collection(collection_name)

    query = {}
    if filter_field and filter_value is not None:
        query[filter_field] = filter_value

    cursor = collection.find(query).limit(limit)

    summaries = []
    for raw_doc in cursor:
        doc_id = str(raw_doc.get("_id", ""))
        data = raw_doc.get("data", {})
        doc_resp = DocumentResponse(
            doc_id=doc_id,
            data=data,
            version=raw_doc.get("version"),
            created_at=raw_doc.get("created_at"),
            updated_at=raw_doc.get("updated_at"),
        )
        summary = summarize_record(doc_resp, client=openai_client)
        summaries.append(summary)

    return summaries


if __name__ == "__main__":
    results = summarize_records_batch(
        collection_name="documents",
        limit=5,
    )
    for r in results:
        print(r)
