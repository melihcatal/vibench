import base64
import json
import os
import sys
from urllib.request import Request, urlopen


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _image_to_data_url(path: str) -> str:
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(path)[1].lower().lstrip(".") or "png"
    mime = "jpeg" if ext in {"jpg", "jpeg"} else ext
    return f"data:image/{mime};base64,{encoded}"


def extract_text(image_path: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all plain text from this scanned document image. Return only the text."},
                    {"type": "input_image", "image_url": _image_to_data_url(image_path)},
                ],
            }
        ],
    }
    req = Request(
        OPENAI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    texts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                texts.append(content.get("text", ""))
    if texts:
        return "".join(texts).strip()
    return data.get("output_text", "").strip()


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: python extract_text.py <image_path>")
    print(extract_text(sys.argv[1]))


if __name__ == "__main__":
    main()
