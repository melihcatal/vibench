import os
import json
from openai import OpenAI
from database_models import FetchResponse, QueryResponse


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o"


def summarize_records(records: list[dict]) -> dict:
    client = OpenAI(api_key=OPENAI_API_KEY)

    records_text = json.dumps(records, indent=2, default=str)

    prompt = (
        "Summarize the following document records in a concise format. "
        "Provide a brief overview of the key themes, common fields, "
        "and any notable patterns. Return the summary as a structured JSON object "
        "with keys: 'overview', 'key_themes', 'common_fields', 'notable_patterns'.\n\n"
        f"Records:\n{records_text}"
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a document analysis assistant that summarizes records.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary_text = response.choices[0].message.content

    try:
        summary_json = json.loads(summary_text)
    except json.JSONDecodeError:
        summary_json = {
            "overview": summary_text,
            "key_themes": [],
            "common_fields": [],
            "notable_patterns": [],
        }

    return {
        "model": OPENAI_MODEL,
        "provider": "openai",
        "summary": summary_json,
        "record_count": len(records),
    }


def summarize_from_fetch_response(fetch_response: FetchResponse) -> dict:
    if not fetch_response.found or not fetch_response.data:
        return {
            "model": OPENAI_MODEL,
            "provider": "openai",
            "summary": {
                "overview": "No document found.",
                "key_themes": [],
                "common_fields": [],
                "notable_patterns": [],
            },
            "record_count": 0,
        }
    return summarize_records([fetch_response.data])


def summarize_from_query_response(query_response: QueryResponse) -> dict:
    records = [item.data for item in query_response.items]
    return summarize_records(records)


if __name__ == "__main__":
    sample_records = [
        {
            "_id": "doc-001",
            "title": "Project Alpha",
            "status": "active",
            "priority": "high",
        },
        {
            "_id": "doc-002",
            "title": "Project Beta",
            "status": "active",
            "priority": "medium",
        },
        {
            "_id": "doc-003",
            "title": "Project Gamma",
            "status": "archived",
            "priority": "low",
        },
    ]
    result = summarize_records(sample_records)
    print(json.dumps(result, indent=2))
