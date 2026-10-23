import os
import json
import dashscope
from dashscope import Generation
from typing import List, Dict, Optional


dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY", "")


def build_usage_prompt(
    key_ids: List[str], usage_events: List[Dict], start_date: str, end_date: str
) -> str:
    event_summary = json.dumps(usage_events, indent=2)
    prompt = (
        f"Summarize the AWS KMS key usage events for the following keys between {start_date} and {end_date}.\n\n"
        f"Key IDs: {', '.join(key_ids)}\n\n"
        f"Usage events:\n{event_summary}\n\n"
        "Provide a concise summary including:\n"
        "1. Total number of operations per key\n"
        "2. Most frequently used keys\n"
        "3. Any unusual patterns or anomalies\n"
        "4. Recommendations for key rotation if applicable\n"
    )
    return prompt


def summarize_key_usage(
    key_ids: Optional[List[str]] = None,
    usage_events: Optional[List[Dict]] = None,
    start_date: str = "",
    end_date: str = "",
    model: str = "qwen-plus",
) -> Dict:
    if usage_events is None:
        usage_events = []
    if key_ids is None:
        key_ids = []

    prompt = build_usage_prompt(key_ids, usage_events, start_date, end_date)

    response = Generation.call(
        model=model,
        prompt=prompt,
        result_format="message",
    )

    if response.status_code == 200:
        summary_text = response.output.choices[0].message.content
    else:
        summary_text = f"Error generating summary: {response.code} - {response.message}"

    key_counts = {}
    for event in usage_events:
        kid = event.get("key_id", "unknown")
        key_counts[kid] = key_counts.get(kid, 0) + 1

    return {
        "summary_text": summary_text,
        "total_events": len(usage_events),
        "key_usage_counts": key_counts,
        "request_id": response.request_id if hasattr(response, "request_id") else "",
    }


if __name__ == "__main__":
    sample_events = [
        {
            "key_id": "arn:aws:kms:us-east-1:123456789012:key/abc123",
            "operation": "Encrypt",
            "timestamp": "2024-01-15T10:00:00Z",
        },
        {
            "key_id": "arn:aws:kms:us-east-1:123456789012:key/abc123",
            "operation": "Decrypt",
            "timestamp": "2024-01-15T10:05:00Z",
        },
        {
            "key_id": "arn:aws:kms:us-east-1:123456789012:key/def456",
            "operation": "GenerateDataKey",
            "timestamp": "2024-01-15T11:00:00Z",
        },
    ]
    result = summarize_key_usage(
        key_ids=["arn:aws:kms:us-east-1:123456789012:key/abc123"],
        usage_events=sample_events,
        start_date="2024-01-01",
        end_date="2024-01-31",
    )
    print(result)
