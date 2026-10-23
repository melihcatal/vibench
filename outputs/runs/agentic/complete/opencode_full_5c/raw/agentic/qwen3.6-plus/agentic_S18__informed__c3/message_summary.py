import json
import os
from typing import Optional
from openai import OpenAI


MODEL_ID = "gpt-4o-mini"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def summarize_processing_results(
    processing_records: list[dict],
    summary_length: str = "concise",
) -> dict:
    if not OPENAI_API_KEY:
        return {
            "success": False,
            "error": "OPENAI_API_KEY environment variable is not set",
            "summary": "",
        }

    records_text = json.dumps(processing_records, indent=2, default=str)
    length_instruction = {
        "concise": "Provide a brief 2-3 sentence summary.",
        "detailed": "Provide a detailed paragraph-by-paragraph summary covering all aspects.",
        "bullet": "Provide a bulleted list of key findings.",
    }.get(summary_length, "Provide a brief summary.")

    prompt = (
        f"Summarize the following message processing results. {length_instruction}\n\n"
        f"Processing Results:\n{records_text}\n\n"
        f"Include: total messages processed, success rate, common error patterns, and any notable trends."
    )

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {
                    "role": "system",
                    "content": "You are a data analyst summarizing message processing results.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=500,
        )
        summary_text = response.choices[0].message.content.strip()
        return {
            "success": True,
            "summary": summary_text,
            "model_used": MODEL_ID,
            "records_count": len(processing_records),
        }
    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "summary": "",
        }


def main():
    sample_records = [
        {"message_id": "msg-001", "status": "processed", "latency_ms": 45},
        {"message_id": "msg-002", "status": "failed", "error": "timeout"},
        {"message_id": "msg-003", "status": "processed", "latency_ms": 32},
    ]
    result = summarize_processing_results(sample_records)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
