import base64
import json
import os
import sys
from typing import Any, Dict
from urllib import request


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_VISION_MODEL = os.environ.get("OPENAI_VISION_MODEL", "gpt-4.1-mini")


def _image_format(image_path: str) -> str:
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    if ext in {"jpg", "jpeg", "png", "webp", "gif"}:
        return "jpeg" if ext == "jpg" else ext
    return "png"


def _image_to_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:image/{_image_format(image_path)};base64,{encoded}"


def _extract_text(response_data: Dict[str, Any]) -> str:
    texts = []
    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    texts.append(text)
    return "\n".join(texts).strip()


def check_visual_safety_text(image_path: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_VISION_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Check all visible text in this image for unsafe, hateful, sexual, violent, self-harm, or other policy-sensitive content. Return strict JSON with keys unsafe (boolean), categories (object with booleans for hateful, sexual, violent, self_harm, harassment, drugs, weapons, minors, other), and summary (short string).",
                    },
                    {"type": "input_image", "image_url": _image_to_data_url(image_path)},
                ],
            }
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }

    req = request.Request(
        f"{OPENAI_API_BASE.rstrip('/')}/responses",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    text = _extract_text(data)
    if not text:
        return json.dumps({"unsafe": False, "categories": {}, "summary": ""})
    return text


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python visual_safety_text.py <image_path>")
    print(check_visual_safety_text(sys.argv[1]))
