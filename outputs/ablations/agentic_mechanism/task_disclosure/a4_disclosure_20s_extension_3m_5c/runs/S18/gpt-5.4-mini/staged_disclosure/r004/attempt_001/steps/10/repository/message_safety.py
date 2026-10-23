import os
import json
import urllib.request
import urllib.error


OPENAI_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_message_payload_text(payload):
    if isinstance(payload, str):
        text = payload
    elif isinstance(payload, dict):
        text = payload.get("text", "")
        if not isinstance(text, str):
            text = str(text)
    else:
        text = str(payload)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    body = json.dumps({"model": OPENAI_MODERATION_MODEL, "input": text}).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_API_URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"OpenAI moderation request failed: {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenAI moderation request failed: {exc.reason}") from exc

    if not result.get("results"):
        raise RuntimeError("OpenAI moderation returned no results")

    moderation = result["results"][0]
    flagged = bool(moderation.get("flagged", False))
    categories = moderation.get("categories", {})
    category_scores = moderation.get("category_scores", {})

    return {
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
    }
