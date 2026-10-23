import os
from datetime import datetime, timezone

from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel

from messaging_models import ConsumeResult, SafetyCheckResult, extract_text_from_payload


SAFETY_MODEL = "gemini-1.5-flash-001"


def check_message_safety(
    consume_result: ConsumeResult,
    project_id: str | None = None,
    location: str = "us-central1",
) -> SafetyCheckResult:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")

    aiplatform.init(project=project_id, location=location)

    text = extract_text_from_payload(consume_result.event.payload)
    prompt = (
        "Analyze the following message content for unsafe or harmful material. "
        "Return a JSON object with these keys: is_safe (boolean), "
        "and scores for categories: violence, hate_speech, sexual, self_harm, harassment "
        "(each a float from 0.0 to 1.0).\n\n"
        f"Message: {text}"
    )

    model = GenerativeModel(SAFETY_MODEL)
    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 128,
            "temperature": 0.1,
        },
    )

    import json

    raw = response.text.strip()
    try:
        analysis = json.loads(raw)
    except json.JSONDecodeError:
        analysis = {
            "is_safe": True,
            "violence": 0.0,
            "hate_speech": 0.0,
            "sexual": 0.0,
            "self_harm": 0.0,
            "harassment": 0.0,
        }

    is_safe = analysis.get("is_safe", True)
    categories = {
        "violence": float(analysis.get("violence", 0.0)),
        "hate_speech": float(analysis.get("hate_speech", 0.0)),
        "sexual": float(analysis.get("sexual", 0.0)),
        "self_harm": float(analysis.get("self_harm", 0.0)),
        "harassment": float(analysis.get("harassment", 0.0)),
    }

    return SafetyCheckResult(
        message_id=consume_result.message_id,
        is_safe=is_safe,
        categories=categories,
        model_used=SAFETY_MODEL,
        checked_at=datetime.now(timezone.utc).isoformat(),
    )


if __name__ == "__main__":
    from messaging_models import EventMessage, ConsumeResult

    event = EventMessage.create(
        event_type="user.message",
        source="chat-service",
        payload={"text": "Hello, how can I help you today?"},
    )
    consume = ConsumeResult(
        message_id="msg-safety-001",
        event=event,
        ack_id="ack-safety-001",
        delivery_attempt=1,
        received_at=datetime.now(timezone.utc).isoformat(),
    )
    result = check_message_safety(consume)
    print(result.to_dict())
