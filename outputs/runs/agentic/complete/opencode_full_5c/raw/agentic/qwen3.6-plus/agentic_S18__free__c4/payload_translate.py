import os
from datetime import datetime, timezone

from google.cloud import translate_v2 as translate

from messaging_models import ConsumeResult, TranslationResult, extract_text_from_payload


TRANSLATION_MODEL = "nmt"


def translate_payload(
    consume_result: ConsumeResult,
    target_language: str = "en",
    project_id: str | None = None,
) -> TranslationResult:
    project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")

    text = extract_text_from_payload(consume_result.event.payload)

    client = translate.Client()

    result = client.translate(
        text,
        target_language=target_language,
        format_="text",
        model=TRANSLATION_MODEL,
    )

    translated_text = result.get("translatedText", text)
    detected_source = result.get("detectedSourceLanguage", "unknown")

    return TranslationResult(
        message_id=consume_result.message_id,
        original_text=text,
        translated_text=translated_text,
        source_language=detected_source,
        target_language=target_language,
        model_used=TRANSLATION_MODEL,
        translated_at=datetime.now(timezone.utc).isoformat(),
    )


if __name__ == "__main__":
    from messaging_models import EventMessage, ConsumeResult

    event = EventMessage.create(
        event_type="support.ticket",
        source="support-system",
        payload={"text": "Bonjour, j'ai un problème avec ma commande."},
    )
    consume = ConsumeResult(
        message_id="msg-translate-001",
        event=event,
        ack_id="ack-translate-001",
        delivery_attempt=1,
        received_at=datetime.now(timezone.utc).isoformat(),
    )
    result = translate_payload(consume, target_language="en")
    print(result.to_dict())
