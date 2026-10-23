import os
import json
from openai import OpenAI
from database_models import DocumentResponse


def summarize_documents(documents, max_tokens=500, model="gpt-4o-mini"):
    api_key = os.environ.get("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    doc_entries = []
    for doc in documents:
        if isinstance(doc, DocumentResponse):
            doc_entries.append(
                {
                    "id": doc.document_id,
                    "data": doc.data,
                }
            )
        elif isinstance(doc, dict):
            doc_entries.append(doc)

    content_text = json.dumps(doc_entries, indent=2, default=str)

    system_prompt = (
        "You are a document summarization assistant. Provide a concise summary of the provided document records. "
        "Highlight key fields, notable values, and any patterns across the documents. "
        "Keep the summary under 300 words."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Summarize these document records:\n\n{content_text}",
            },
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    summary_text = response.choices[0].message.content.strip()

    return {
        "summary": summary_text,
        "model_used": model,
        "document_count": len(doc_entries),
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
    }
