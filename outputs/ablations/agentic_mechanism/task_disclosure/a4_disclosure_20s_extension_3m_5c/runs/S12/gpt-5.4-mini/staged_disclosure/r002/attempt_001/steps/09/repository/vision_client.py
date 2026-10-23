import base64
import json
import mimetypes
import os
from dataclasses import dataclass
from typing import Any
from urllib import error, request

OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = os.environ.get("VISION_CLIENT_MODEL", "gpt-4.1-mini")


@dataclass(frozen=True)
class VisionClientConfig:
    api_key: str
    model: str = OPENAI_MODEL
    timeout: int = 60


def load_config() -> VisionClientConfig:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    model = os.environ.get("VISION_CLIENT_MODEL", OPENAI_MODEL)
    timeout = int(os.environ.get("VISION_CLIENT_TIMEOUT", "60"))
    return VisionClientConfig(api_key=api_key, model=model, timeout=timeout)


def image_data_uri(image_path: str) -> str:
    mime, _ = mimetypes.guess_type(image_path)
    if mime is None:
        mime = "application/octet-stream"
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _image_format(image_path: str) -> str:
    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    if ext in {"jpg", "jpeg", "png", "webp", "gif"}:
        return "jpeg" if ext == "jpg" else ext
    return "png"


def _post_json(url: str, payload: dict[str, Any], api_key: str, timeout: int) -> dict[str, Any]:
    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        raise RuntimeError(f"OpenAI API request failed: {exc.code} {detail}") from exc


def _extract_output_text(response_data: dict[str, Any]) -> str:
    texts: list[str] = []
    for item in response_data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                text = content.get("text")
                if text:
                    texts.append(text)
    return "\n".join(texts).strip()


def describe_image(image_path: str, config: VisionClientConfig | None = None) -> str:
    config = config or load_config()
    payload = {
        "model": config.model,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Write a short visual description of this image in one sentence."},
                    {"type": "input_image", "image_url": image_data_uri(image_path)},
                ],
            }
        ],
    }
    response = _post_json(OPENAI_API_URL, payload, config.api_key, config.timeout)
    return _extract_output_text(response)


def extract_visible_text(image_path: str, config: VisionClientConfig | None = None) -> str:
    config = config or load_config()
    payload = {
        "model": config.model,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Extract all visible text from this image. Return only the text."},
                    {"type": "input_image", "image_url": f"data:image/{_image_format(image_path)};base64,{base64.b64encode(open(image_path, 'rb').read()).decode('ascii')}"},
                ],
            }
        ],
    }
    response = _post_json(OPENAI_API_URL, payload, config.api_key, config.timeout)
    return _extract_output_text(response)


def analyze_image(image_path: str, prompt: str, config: VisionClientConfig | None = None) -> str:
    config = config or load_config()
    payload = {
        "model": config.model,
        "input": [
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {"type": "input_image", "image_url": image_data_uri(image_path)},
                ],
            }
        ],
    }
    response = _post_json(OPENAI_API_URL, payload, config.api_key, config.timeout)
    return _extract_output_text(response)
