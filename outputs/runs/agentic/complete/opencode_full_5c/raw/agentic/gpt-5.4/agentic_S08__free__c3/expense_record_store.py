from __future__ import annotations

import os
from typing import Any, Dict

import requests


NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_VERSION = os.getenv("NOTION_VERSION", "2022-06-28")
NOTION_PAGES_URL = "https://api.notion.com/v1/pages"


def expense_record_store(expense_record: Dict[str, Any]) -> Dict[str, Any]:
    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        raise ValueError("NOTION_API_KEY and NOTION_DATABASE_ID are required")
    title = (
        expense_record.get("vendor")
        or expense_record.get("merchant")
        or "Expense Record"
    )
    total = expense_record.get("total")
    document_date = expense_record.get("document_date")
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": str(title)}}]},
            "Document Date": {"date": {"start": document_date}}
            if document_date
            else {"date": None},
            "Total": {"number": total},
            "Source Type": {
                "rich_text": [
                    {
                        "text": {
                            "content": str(
                                expense_record.get("source_document_type", "unknown")
                            )
                        }
                    }
                ]
            },
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": str(expense_record)},
                        }
                    ]
                },
            }
        ],
    }
    response = requests.post(
        NOTION_PAGES_URL,
        headers={
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return {"id": data.get("id"), "url": data.get("url"), "object": data.get("object")}
