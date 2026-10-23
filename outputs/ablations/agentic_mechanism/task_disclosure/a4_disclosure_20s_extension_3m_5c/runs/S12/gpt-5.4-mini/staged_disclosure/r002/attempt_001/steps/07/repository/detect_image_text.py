import base64
import json
import os
import sys
from urllib import request


def detect_image_text(image_path: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    with open(image_path, "rb") as f:
        image_data = f.read()

    payload = {
        "model": "gpt-4.1-mini",
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all visible text from this image. Return only the text."},
                    {
                        "type": "input_image",
                        "image_url": f"data:image/{_image_format(image_path)};base64,{base64.b64encode(image_data).decode('ascii')}"
                    },
                ],
            }
        ],
    }

    req = request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return _extract_text(data)


def _extract_text(response_data: dict) -> str:
    texts = []
    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    texts.append(text)
    return "\n".join(texts).strip()


def _image_format(image_path: str) -> str:
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    if ext in {"jpg", "jpeg", "png", "webp", "gif"}:
        return "jpeg" if ext == "jpg" else ext
    return "png"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python detect_image_text.py <image_path>")
    print(detect_image_text(sys.argv[1]))
