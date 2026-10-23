import os
from deepl import Translator
from datetime import datetime
from uuid import uuid4
from messaging_models import MessageEvent, MessagePayload


def translate_message(event: MessageEvent, target_lang: str = "ES") -> str:
    translator = Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(event.payload.message, target_lang=target_lang)
    return result.text


if __name__ == "__main__":
    event = MessageEvent(
        event_id=str(uuid4()),
        timestamp=datetime.utcnow().isoformat(),
        payload=MessagePayload(
            customer_name="Global Customer",
            order_id="TRANS-101",
            message="I need help with my recent purchase.",
        ),
    )
    translated = translate_message(event)
    print(f"Translated to Spanish: {translated}")
