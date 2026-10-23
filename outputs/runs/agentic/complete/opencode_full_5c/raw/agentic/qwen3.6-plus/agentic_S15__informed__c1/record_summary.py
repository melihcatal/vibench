import os
import json
from openai import OpenAI
from database_models import DocumentResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"


def summarize_documents(documents: list[DocumentResponse]) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    doc_texts = []
    for doc in documents:
        doc_texts.append(
            f"Document {doc.document_id} (collection: {doc.collection}):\n{json.dumps(doc.data, indent=2)}"
        )
    combined = "\n\n".join(doc_texts)
    system_prompt = (
        "You are a document summarization assistant. "
        "Provide a concise summary of the provided document records, "
        "highlighting key fields, patterns, and notable content."
    )
    user_prompt = f"Summarize the following document records:\n\n{combined}"
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()
