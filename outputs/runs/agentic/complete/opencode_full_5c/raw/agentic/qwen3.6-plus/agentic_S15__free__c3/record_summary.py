import os
import json
import requests
from typing import List, Optional
from database_models import DocumentResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def summarize_documents(
    documents: List[DocumentResponse],
    max_length: int = 500,
    focus: Optional[str] = None,
) -> str:
    if not documents:
        return "No documents to summarize."
    doc_contents = []
    for doc in documents:
        content = {
            "id": doc.document_id,
            "collection": doc.collection,
            "data": doc.data,
        }
        doc_contents.append(content)
    prompt_parts = [
        f"Summarize the following {len(documents)} document records from a NoSQL document store.",
        f"Keep the summary under {max_length} characters.",
    ]
    if focus:
        prompt_parts.append(f"Focus specifically on: {focus}")
    prompt_parts.append("")
    prompt_parts.append(json.dumps(doc_contents, indent=2, default=str))
    system_prompt = "You are a document summarization assistant. Provide concise, factual summaries of structured document data."
    user_prompt = "\n".join(prompt_parts)
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 1024,
        "temperature": 0.3,
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    result = response.json()
    summary = result["choices"][0]["message"]["content"]
    return summary


if __name__ == "__main__":
    sample_docs = [
        DocumentResponse(
            document_id="user_001",
            data={"name": "Alice", "email": "alice@example.com", "role": "admin"},
            collection="users",
            version=2,
        ),
        DocumentResponse(
            document_id="user_002",
            data={"name": "Bob", "email": "bob@example.com", "role": "user"},
            collection="users",
            version=1,
        ),
    ]
    summary = summarize_documents(
        sample_docs, focus="user roles and contact information"
    )
    print(summary)
