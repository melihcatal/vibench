import os
import deepl
from datetime import datetime, timedelta
from typing import List, Dict
from observability_client import ObservabilityClient


def log_message_translate(
    hours_back: int = 1, target_lang: str = "FR"
) -> List[Dict[str, str]]:
    client = ObservabilityClient()
    now = datetime.utcnow()
    to_ts = int(now.timestamp() * 1000)
    from_ts = int((now - timedelta(hours=hours_back)).timestamp() * 1000)
    logs = client.query_logs("@status:(error OR warn)", from_ts, to_ts, 20)

    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))

    translated = []
    for log in logs:
        attrs = log.get("attributes", {})
        original = attrs.get("message", "")
        if original:
            result = translator.translate_text(original, target_lang=target_lang)
            translated.append(
                {
                    "log_id": log.get("id"),
                    "original": original,
                    "translated": result.text,
                }
            )

    return translated
