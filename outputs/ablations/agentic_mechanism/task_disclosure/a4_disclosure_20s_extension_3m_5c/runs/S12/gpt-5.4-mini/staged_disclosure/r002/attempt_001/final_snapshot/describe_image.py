import base64
import mimetypes
import os
import sys
from urllib import request, error

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _image_data_uri(path: str) -> tuple[str, str]:
    mime, _ = mimetypes.guess_type(path)
    if mime is None:
        mime = "application/octet-stream"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{data}", mime


def describe_image(image_path: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    image_uri, _ = _image_data_uri(image_path)
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Write a short visual description of this image in one sentence."},
                    {"type": "image_url", "image_url": {"url": image_uri}},
                ],
            }
        ],
        "max_tokens": 60,
    }

    req = request.Request(
        OPENAI_API_URL,
        data=__import__("json").dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(req, timeout=60) as resp:
            data = __import__("json").loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"OpenAI API request failed: {exc.code} {detail}") from exc

    return data["choices"][0]["message"]["content"].strip()


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python describe_image.py <image_path>")
    print(describe_image(sys.argv[1]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
