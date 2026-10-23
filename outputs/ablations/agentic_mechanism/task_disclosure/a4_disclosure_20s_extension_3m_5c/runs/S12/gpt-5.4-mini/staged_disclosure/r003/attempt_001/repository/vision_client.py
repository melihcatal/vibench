import base64
import json
import os
import urllib.error
import urllib.request


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def get_openai_api_key() -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return api_key


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def image_to_data_url(image_path: str, mime_type: str = "image/jpeg") -> str:
    image_b64 = base64.b64encode(load_image_bytes(image_path)).decode("ascii")
    return f"data:{mime_type};base64,{image_b64}"


def _extract_output_text(result: dict) -> str:
    text_parts = []
    for item in result.get("output", []):
        for content in item.get("content", []):
            if content.get("type") == "output_text":
                text_parts.append(content.get("text", ""))
    return "\n".join(part for part in text_parts if part).strip()


def _post_openai_responses(payload: dict) -> dict:
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OPENAI_API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {get_openai_api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(e.read().decode("utf-8", errors="replace")) from e


def describe_static_image(image_path: str) -> str:
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Write one short visual description of this image in a single sentence."},
                    {"type": "input_image", "image_url": image_to_data_url(image_path)},
                ],
            }
        ],
    }
    return _extract_output_text(_post_openai_responses(payload))


def understand_image(image_path: str, prompt: str) -> str:
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": image_to_data_url(image_path)},
                ],
            }
        ],
    }
    return _extract_output_text(_post_openai_responses(payload))
