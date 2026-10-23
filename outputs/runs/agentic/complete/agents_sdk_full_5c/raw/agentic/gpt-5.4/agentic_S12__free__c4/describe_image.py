from __future__ import annotations

from typing import Dict
from urllib.parse import urlencode

from vision_client import GOOGLE_GEMINI_ENDPOINT, build_gemini_parts, get_env, parse_gemini_text, post_json
from vision_models import VisualDescription


PROVIDER = "google_gemini"
MODEL = "gemini-1.5-flash"


def describe_image(image_path: str, prompt: str = "Write one short, factual sentence describing this image.", mime_type: str = "image/jpeg") -> Dict[str, str]:
    api_key = get_env("GOOGLE_API_KEY")
    url = f"{GOOGLE_GEMINI_ENDPOINT}?{urlencode({'key': api_key})}"
    payload = build_gemini_parts(prompt=prompt, image_path=image_path, mime_type=mime_type)
    response = post_json(url, payload)
    description = VisualDescription(text=parse_gemini_text(response), model=MODEL, provider=PROVIDER)
    return {"text": description.text, "model": description.model, "provider": description.provider}
