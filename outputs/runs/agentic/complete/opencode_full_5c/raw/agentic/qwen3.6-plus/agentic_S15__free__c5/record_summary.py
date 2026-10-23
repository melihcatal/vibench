import os
import json
from openai import OpenAI
from database_models import DocumentResponse, SummaryRecord

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"


def summarize_records(documents: list[DocumentResponse]) -> list[SummaryRecord]:
    client = OpenAI(api_key=OPENAI_API_KEY)
    summaries = []

    for doc in documents:
        content = json.dumps(doc.data, default=str)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Summarize the following document content concisely in 2-3 sentences.",
                },
                {"role": "user", "content": content},
            ],
            max_tokens=200,
        )
        summary_text = response.choices[0].message.content.strip()
        summaries.append(
            SummaryRecord(
                document_id=doc.document_id,
                summary=summary_text,
                source_fields=list(doc.data.keys()),
            )
        )

    return summaries
