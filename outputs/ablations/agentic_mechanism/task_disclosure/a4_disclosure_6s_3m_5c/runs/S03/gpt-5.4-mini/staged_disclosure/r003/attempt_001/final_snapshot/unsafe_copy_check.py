import json
import os
import sys
import urllib.request


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def check_unsafe_copy(text: str) -> dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = json.dumps({"model": "omni-moderation-latest", "input": text}).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_MODERATION_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode("utf-8"))

    result = data["results"][0]
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    unsafe = bool(result.get("flagged", False))
    return {
        "unsafe": unsafe,
        "categories": categories,
        "category_scores": category_scores,
    }


def main() -> None:
    text = sys.stdin.read()
    if not text:
        raise SystemExit("No input provided")
    print(json.dumps(check_unsafe_copy(text), ensure_ascii=False))


if __name__ == "__main__":
    main()
