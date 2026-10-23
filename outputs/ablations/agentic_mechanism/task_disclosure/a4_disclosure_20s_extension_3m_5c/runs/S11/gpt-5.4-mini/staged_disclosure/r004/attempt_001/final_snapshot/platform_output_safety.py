import os
import json
import urllib.request
import urllib.error


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODEL = "omni-moderation-latest"


def check_platform_output_safety(text):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = json.dumps({"model": OPENAI_MODEL, "input": text}).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_MODERATION_URL,
        data=payload,
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
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI moderation request failed: {exc.code} {body}") from exc

    outputs = result.get("results", [])
    if not outputs:
        raise RuntimeError("OpenAI moderation returned no results")

    outcome = outputs[0]
    flagged = bool(outcome.get("flagged"))
    categories = outcome.get("categories", {})
    category_scores = outcome.get("category_scores", {})

    return {
        "safe": not flagged,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "raw": outcome,
    }
