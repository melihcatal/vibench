import os
import json
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def summarize_documents(documents: list, max_length: int = 200) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)

    doc_texts = []
    for doc in documents:
        if hasattr(doc, "to_dict"):
            doc_data = doc.to_dict()
        else:
            doc_data = doc
        data = doc_data.get("data", doc_data)
        if isinstance(data, str):
            data = json.loads(data)
        text_parts = []
        for key, value in data.items():
            if isinstance(value, str) and len(value) > 10:
                text_parts.append(f"{key}: {value}")
        if text_parts:
            doc_texts.append("; ".join(text_parts))

    if not doc_texts:
        return "No document content available for summarization."

    combined_text = "\n---\n".join(doc_texts)

    prompt = (
        f"Summarize the following document records in a concise paragraph "
        f"(maximum {max_length} words):\n\n{combined_text}"
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a document summarization assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.3,
    )

    summary = response.choices[0].message.content.strip()
    return summary
