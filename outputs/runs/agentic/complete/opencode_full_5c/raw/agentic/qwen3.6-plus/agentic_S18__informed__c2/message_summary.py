import os
import json
from dashscope import Generation


def summarize_processing_results(
    processing_records: list[dict],
    model: str = "qwen-plus",
) -> dict:
    api_key = os.getenv("DASHSCOPE_API_KEY", "")
    if not api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable is required")

    records_summary = json.dumps(processing_records, indent=2)
    prompt = (
        f"Summarize the following message processing results. "
        f"Provide a concise overview including total messages processed, "
        f"success rate, common event types, any errors encountered, "
        f"and key observations.\n\n"
        f"Processing Records:\n{records_summary}"
    )

    response = Generation.call(
        api_key=api_key,
        model=model,
        messages=[{"role": "user", "content": prompt}],
        result_format="message",
    )

    if response.status_code == 200:
        summary_text = response.output.choices[0].message.content
        return {
            "summary": summary_text,
            "model_used": model,
            "status": "success",
            "record_count": len(processing_records),
        }
    else:
        return {
            "summary": "",
            "model_used": model,
            "status": "error",
            "error": response.message,
            "record_count": len(processing_records),
        }


if __name__ == "__main__":
    sample_records = [
        {
            "event_id": "evt-001",
            "event_type": "order.created",
            "status": "success",
            "processing_time_ms": 45,
        },
        {
            "event_id": "evt-002",
            "event_type": "payment.processed",
            "status": "success",
            "processing_time_ms": 120,
        },
        {
            "event_id": "evt-003",
            "event_type": "order.created",
            "status": "failed",
            "error": "timeout",
        },
        {
            "event_id": "evt-004",
            "event_type": "user.signup",
            "status": "success",
            "processing_time_ms": 30,
        },
    ]
    result = summarize_processing_results(sample_records)
    print(json.dumps(result, indent=2))
