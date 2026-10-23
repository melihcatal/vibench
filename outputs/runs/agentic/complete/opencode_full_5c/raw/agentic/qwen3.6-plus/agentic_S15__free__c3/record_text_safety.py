import os
import requests
from typing import List, Dict, Optional
from database_models import DocumentResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_text_safety(text: str) -> Dict:
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
        "model": OPENAI_MODERATION_MODEL,
    }
    response = requests.post(
        OPENAI_MODERATION_URL, headers=headers, json=payload, timeout=30
    )
    response.raise_for_status()
    result = response.json()
    moderation_result = result["results"][0]
    return {
        "flagged": moderation_result["flagged"],
        "categories": moderation_result["categories"],
        "category_scores": moderation_result["category_scores"],
    }


def check_document_safety(
    documents: List[DocumentResponse],
    fields_to_check: Optional[List[str]] = None,
) -> List[Dict]:
    if fields_to_check is None:
        fields_to_check = [
            "name",
            "email",
            "content",
            "description",
            "comment",
            "title",
            "body",
        ]
    safety_results = []
    for doc in documents:
        doc_safety = {
            "document_id": doc.document_id,
            "collection": doc.collection,
            "fields_checked": [],
            "any_flagged": False,
            "details": [],
        }
        for field_name in fields_to_check:
            field_value = doc.data.get(field_name)
            if field_value is None:
                continue
            text_value = str(field_value)
            if not text_value.strip():
                continue
            safety = check_text_safety(text_value)
            doc_safety["fields_checked"].append(field_name)
            doc_safety["details"].append(
                {
                    "field": field_name,
                    "flagged": safety["flagged"],
                    "categories": {k: v for k, v in safety["categories"].items() if v},
                }
            )
            if safety["flagged"]:
                doc_safety["any_flagged"] = True
        safety_results.append(doc_safety)
    return safety_results


if __name__ == "__main__":
    sample_docs = [
        DocumentResponse(
            document_id="post_001",
            data={"title": "Hello World", "body": "This is a friendly post."},
            collection="posts",
            version=1,
        ),
    ]
    results = check_document_safety(sample_docs)
    for r in results:
        print(r)
