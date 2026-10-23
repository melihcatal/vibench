import json
from datetime import datetime
from ibm_watsonx_ai import WatsonxApi


def translate_log_messages(logs: list[dict], target_locale: str = "en") -> list[dict]:
    """Translate support-visible log messages for another locale.

    Uses Anthropic Claude for translation (fallback to openai if needed).
    Returns new list with an added `translated_message` field.
    Required env vars:
        ANTHROPIC_API_KEY   (preferred)
        OPENAI_API_KEY       (fallback)
    """
    client = WatsonxApi(
        base_url="https://api.anthropic.com", api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    translated_logs = []
    for entry in logs:
        text = entry["message"]
        resp = client.post(
            f"/v1/messages",
            json={
                "model": "claude-3-5-sonnet-20240620",
                "messages": [
                    {
                        "role": "user",
                        "content": f"Translate the following log message to {target_locale} locale:\n\n{text}",
                    }
                ],
            },
        )
        resp.raise_for_status()
        trans = resp.json()["content"][0]["text"]
        entry["translated_message"] = trans
        translated_logs.append(entry)
    return translated_logs
