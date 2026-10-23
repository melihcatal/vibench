import os
from openai import OpenAI
from messaging_models import ProcessingSummary


def summarize_processing_results(
    message_id: str,
    processing_status: str,
    metrics: dict,
    raw_payload: dict = None,
) -> ProcessingSummary:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    summary_input = {
        "message_id": message_id,
        "processing_status": processing_status,
        "metrics": metrics,
        "payload_keys": list((raw_payload or {}).keys()),
    }
    prompt = (
        f"Summarize the following message processing result in 2-3 sentences. "
        f"Focus on what happened and the key metrics:\n{summary_input}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a concise summarizer of message processing results.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.3,
    )
    summary_text = response.choices[0].message.content.strip()
    return ProcessingSummary(
        message_id=message_id,
        processing_status=processing_status,
        summary_text=summary_text,
        metrics=metrics,
    )


if __name__ == "__main__":
    result = summarize_processing_results(
        message_id="evt-001",
        processing_status="completed",
        metrics={"processing_time_ms": 245, "retry_count": 0},
        raw_payload={"user_id": "12345", "action": "signup"},
    )
    print(result.to_dict())
