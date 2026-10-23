import os
import requests

TISANE_API_URL = os.getenv("TISANE_API_URL", "https://api.tisane.ai/text/1.0/moderate")
TISANE_API_KEY_ENV = "TISANE_API_KEY"


def check_corpus_safety(
    texts: list[str],
    api_key: str | None = None,
    categories: list[str] | None = None,
) -> list[dict]:
    key = api_key or os.getenv(TISANE_API_KEY_ENV)
    if not key:
        raise ValueError(f"{TISANE_API_KEY_ENV} environment variable is required")
    if categories is None:
        categories = ["hate", "violence", "sexual", "self_harm", "profanity"]
    results = []
    for text in texts:
        payload = {
            "text": text,
            "categories": categories,
        }
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": key,
        }
        resp = requests.post(
            TISANE_API_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        flagged = False
        flags = []
        for category_result in data.get("categories", []):
            cat_name = category_result.get("category", "")
            score = category_result.get("score", 0.0)
            if score > 0.5:
                flagged = True
                flags.append({"category": cat_name, "score": score})
        results.append(
            {
                "text": text,
                "safe": not flagged,
                "flags": flags,
                "raw_response": data,
            }
        )
    return results


def is_corpus_safe(
    text: str,
    api_key: str | None = None,
    threshold: float = 0.5,
) -> bool:
    results = check_corpus_safety([text], api_key=api_key)
    return results[0]["safe"]
