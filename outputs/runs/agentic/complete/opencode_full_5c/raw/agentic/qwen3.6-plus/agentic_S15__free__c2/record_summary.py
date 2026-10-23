import os
from openai import OpenAI
from database_models import DocumentResponse

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"


def summarize_documents(
    documents: list[DocumentResponse], max_length: int = 300
) -> list[dict]:
    client = OpenAI(api_key=OPENAI_API_KEY)

    summaries = []
    for doc in documents:
        content_text = _extract_text_content(doc)
        if not content_text.strip():
            summaries.append(
                {
                    "document_id": doc.document_id,
                    "summary": "",
                }
            )
            continue

        prompt = f"Summarize the following document content in {max_length} characters or fewer:\n\n{content_text}"

        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a concise document summarizer."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=256,
            temperature=0.3,
        )

        summary_text = response.choices[0].message.content.strip()
        summaries.append(
            {
                "document_id": doc.document_id,
                "summary": summary_text,
            }
        )

    return summaries


def _extract_text_content(doc: DocumentResponse) -> str:
    parts = []
    for key, value in doc.data.items():
        if isinstance(value, str):
            parts.append(f"{key}: {value}")
        elif isinstance(value, (list, tuple)):
            items = [str(v) for v in value if isinstance(v, str)]
            if items:
                parts.append(f"{key}: {'; '.join(items)}")
    return "\n".join(parts)
