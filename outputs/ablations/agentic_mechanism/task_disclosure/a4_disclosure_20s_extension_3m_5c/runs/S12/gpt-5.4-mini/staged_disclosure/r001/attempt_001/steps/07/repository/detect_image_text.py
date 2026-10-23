import base64
import json
import os
import sys
from urllib import request, error


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def detect_text(image_path: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode("ascii")

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all visible text from this image. Return only the text."},
                    {"type": "input_image", "image_url": f"data:image/*;base64,{image_data}"},
                ],
            }
        ],
    }

    req = request.Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"OpenAI API error: {exc.code} {body}") from exc

    parts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text", "")
                if text:
                    parts.append(text)
    return "\n".join(parts).strip()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python detect_image_text.py <image_path>")
    print(detect_text(sys.argv[1]))


if __name__ == "__main__":
    main()
