import os
from datetime import datetime, timezone

from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel

from messaging_models import ConsumeResult, MessageSummary, extract_text_from_payload


VERTEX_AI_MODEL = "gemini-1.5-flash-001"


def summarize_message(
    consume_result: ConsumeResult,
    max_tokens: int = 256,
    project_id: str | None = None,
    location: str = "us-central1",
) -> MessageSummary:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")

    aiplatform.init(project=project_id, location=location)

    text = extract_text_from_payload(consume_result.event.payload)
    prompt = (
        f"Summarize the following message from event type '{consume_result.event.event_type}' "
        f"in 2-3 sentences:\n\n{text}"
    )

    model = GenerativeModel(VERTEX_AI_MODEL)
    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": max_tokens,
            "temperature": 0.3,
        },
    )

    summary_text = response.text.strip()
    token_count = (
        response.usage_metadata.total_token_count if response.usage_metadata else 0
    )

    return MessageSummary(
        message_id=consume_result.message_id,
        summary_text=summary_text,
        model_used=VERTEX_AI_MODEL,
        token_count=token_count,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


if __name__ == "__main__":
    from messaging_models import EventMessage, ConsumeResult

    event = EventMessage.create(
        event_type="support.ticket",
        source="support-system",
        payload={
            "text": "Customer unable to access their account after password reset. "
            "They have tried multiple browsers and clearing cache. "
            "Urgent assistance needed."
        },
    )
    consume = ConsumeResult(
        message_id="msg-001",
        event=event,
        ack_id="ack-001",
        delivery_attempt=1,
        received_at=datetime.now(timezone.utc).isoformat(),
    )
    result = summarize_message(consume)
    print(result.to_dict())
