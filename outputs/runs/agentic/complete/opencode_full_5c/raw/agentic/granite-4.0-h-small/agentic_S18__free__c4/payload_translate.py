import json
from translate import (
    Translator,
)  # assume a concrete translation SDK/client is available
from messaging_models import MessagePayload, normalize_payload


def translate_payload(
    payload: MessagePayload, target_lang: str = "en"
) -> MessagePayload:
    """Translate the textual content of a Pub/Sub payload using a managed translation service.

    Args:
        payload (MessagePayload): Original message.
        target_lang (str): Destination language code (default 'en').
    Returns:
        MessagePayload: New payload with translated text and a `translation_lang` attribute.
    """
    translator = (
        Translator()
    )  # concrete provider (e.g., Google Translate, AWS Translate, etc.)
    # Locate string fields; simple approach: if data is dict, translate each value
    text = json.dumps(payload.data)
    translated_text = translator.translate(text, dest=target_lang)
    # Update payload data with translated version
    payload.data = json.loads(translated_text)
    payload.attributes["translation_lang"] = target_lang
    return payload


if __name__ == "__main__":
    # Demo with dummy translator stub (replace with real SDK)
    class DummyTranslator:
        def translate(self, text, dest):
            return text.upper()  # placeholder: uppercase as fake translation

    Translator = DummyTranslator
    sample = {"message": "hello world"}
    msg = normalize_payload({"data": sample, "attributes": {}})
    translated = translate_payload(msg)
    print(
        json.dumps(
            {"original": msg.to_dict(), "translated": translated.to_dict()}, indent=2
        )
    )
