import os
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
DEFAULT_VISION_MODEL = "gpt-4o"
DEFAULT_TEXT_MODEL = "gpt-4o"
DEFAULT_MAX_TOKENS = 300
DEFAULT_TEMPERATURE = 0.0


def get_openai_client(
    api_key: str | None = None, base_url: str | None = None
) -> OpenAI:
    key = api_key or OPENAI_API_KEY
    url = base_url or OPENAI_BASE_URL
    return OpenAI(api_key=key, base_url=url)


def encode_image_to_base64(image_path: str) -> str:
    import base64

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def build_image_url(image_path: str) -> str:
    b64 = encode_image_to_base64(image_path)
    ext = os.path.splitext(image_path)[1].lstrip(".") or "png"
    return f"data:image/{ext};base64,{b64}"


def build_vision_messages(
    system_prompt: str,
    user_prompt: str,
    image_path: str | None = None,
) -> list[dict]:
    messages: list[dict] = [{"role": "system", "content": system_prompt}]
    if image_path:
        image_url = build_image_url(image_path)
        user_content = [
            {"type": "text", "text": user_prompt},
            {
                "type": "image_url",
                "image_url": {"url": image_url, "detail": "high"},
            },
        ]
    else:
        user_content = user_prompt
    messages.append({"role": "user", "content": user_content})
    return messages


def call_vision_api(
    messages: list[dict],
    model: str = DEFAULT_VISION_MODEL,
    max_tokens: int = DEFAULT_MAX_TOKENS,
    temperature: float = DEFAULT_TEMPERATURE,
    client: OpenAI | None = None,
) -> str:
    c = client or get_openai_client()
    response = c.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content or ""
