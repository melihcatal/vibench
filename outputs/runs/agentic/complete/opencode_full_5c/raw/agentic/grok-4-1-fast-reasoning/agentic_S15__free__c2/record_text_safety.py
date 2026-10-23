import os
import json
from openai import OpenAI
from typing import Dict, Any, List


def check_document_fields_safety(
    document: Dict[str, Any], fields: List[str] = None
) -> Dict[str, Any]:
    if fields is None:
        fields = ["content", "title", "description", "body", "text"]
    texts = [
        document.get(f, "")
        for f in fields
        if isinstance(document.get(f), str) and document.get(f)
    ]
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    results = []
    for text in texts:
        if len(text) > 1:
            moderation = client.moderations.create(
                model="text-moderation-3.5-2024-04-09", input=text[:4096]
            )
            results.append(
                {"text_preview": text[:50] + "...", "moderation": moderation.results[0]}
            )
    return {"document_id": document.get("id"), "safety_results": results}
