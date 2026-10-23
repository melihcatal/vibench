import os
import sys
import base64
import json
import urllib.request
import urllib.error


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _load_image_bytes(path):
    with open(path, "rb") as f:
        return f.read()


def detect_text_in_image(image_path):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    image_bytes = _load_image_bytes(image_path)
    image_b64 = base64.b64encode(image_bytes).decode("ascii")
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all visible text from this image. Return only the text."},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{image_b64}"},
                ],
            }
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode("utf-8", errors="replace")) from e

    text_parts = []
    for item in result.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                text_parts.append(content.get("text", ""))
    return "\n".join(part for part in text_parts if part).strip()


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: detect_image_text.py IMAGE_PATH")
    print(detect_text_in_image(sys.argv[1]))


if __name__ == "__main__":
    main()
