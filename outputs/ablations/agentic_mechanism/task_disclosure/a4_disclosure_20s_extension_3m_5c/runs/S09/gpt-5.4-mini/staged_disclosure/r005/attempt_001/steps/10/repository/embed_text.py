import json
import os
import sys
from urllib import request


def embed_text(text: str) -> list[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = json.dumps({"input": text, "model": "text-embedding-3-small"}).encode("utf-8")
    req = request.Request(
        "https://api.openai.com/v1/embeddings",
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["data"][0]["embedding"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python embed_text.py 'text'")
    print(json.dumps(embed_text(sys.argv[1])))
