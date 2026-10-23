import os
import json
from openai import OpenAI
from database_models import RecordSummaryRequest, RecordSummaryResponse

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"


def summarize_record(request: RecordSummaryRequest) -> RecordSummaryResponse:
    client = OpenAI(api_key=OPENAI_API_KEY)

    fields_text = request.to_prompt_fields()
    length_instruction = {
        "short": "2-3 sentences",
        "medium": "one concise paragraph of 4-6 sentences",
        "long": "two detailed paragraphs",
    }.get(request.summary_length, "one concise paragraph")

    system_prompt = (
        "You are a document summarization assistant. "
        "Given a set of document fields, produce a clear and concise summary. "
        f"Keep the summary to {length_instruction}. "
        "Do not add information that is not present in the fields."
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": fields_text},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    summary = response.choices[0].message.content.strip()

    return RecordSummaryResponse(
        document_id=request.document_id,
        summary=summary,
        model_used=OPENAI_MODEL,
    )


def summarize_record_raw(
    document_id: str, data: dict, summary_length: str = "medium"
) -> dict:
    request = RecordSummaryRequest(
        document_id=document_id,
        data=data,
        summary_length=summary_length,
    )
    response = summarize_record(request)
    return response.to_dict()


if __name__ == "__main__":
    result = summarize_record_raw(
        document_id="doc-001",
        data={
            "title": "Quarterly Report",
            "status": "final",
            "author": "Jane Doe",
            "word_count": "4500",
        },
        summary_length="short",
    )
    print(json.dumps(result, indent=2))
