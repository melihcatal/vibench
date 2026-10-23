import os
import sys
import base64
import json
from urllib.request import Request, urlopen


def extract_text(image_path: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    with open(image_path, "rb") as f:
        image_bytes = f.read()
    mime = "image/png"
    lower = image_path.lower()
    if lower.endswith(".jpg") or lower.endswith(".jpeg"):
        mime = "image/jpeg"
    elif lower.endswith(".webp"):
        mime = "image/webp"
    elif lower.endswith(".gif"):
        mime = "image/gif"
    b64 = base64.b64encode(image_bytes).decode("ascii")
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all plain text from this scanned document image. Return only the text."},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                ],
            }
        ],
        "temperature": 0,
    }
    req = Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data["choices"][0]["message"]["content"].strip()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python extract_text.py <image_path>")
    print(extract_text(sys.argv[1]))
