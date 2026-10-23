import json
from typing import Any, Dict

from observability_client import create_openai_client, client_model_name, build_chat_messages


def dashboard_note_translate(text: str, locale: str) -> Dict[str, Any]:
    client = create_openai_client()
    model = client_model_name()
    response = client.chat.completions.create(model=model, messages=build_chat_messages("You translate dashboard notes.", json.dumps({"text": text, "locale": locale})))
    return {"locale": locale, "translation": response.choices[0].message.content if response.choices else "", "provider": "openai", "model": model}
