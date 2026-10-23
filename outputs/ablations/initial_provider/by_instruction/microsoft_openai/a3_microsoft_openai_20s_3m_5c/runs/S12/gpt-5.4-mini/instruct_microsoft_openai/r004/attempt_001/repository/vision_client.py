import base64
import os
from typing import Any, Dict

from openai import OpenAI

from vision_models import VisionRequest, VisionResponse


def load_vision_config() -> Dict[str, Any]:
    return {
        "model": os.getenv("OPENAI_VISION_MODEL", "gpt-5.4-mini"),
        "api_key": os.getenv("OPENAI_API_KEY"),
    }


def build_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def image_data_url(image_path: str) -> str:
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    ext = os.path.splitext(image_path)[1].lower().lstrip(".") or "png"
    mime = f"image/{'jpeg' if ext in {'jpg', 'jpeg'} else ext}"
    return f"data:{mime};base64,{encoded}"


def run_vision_request(req: VisionRequest) -> VisionResponse:
    client = build_client()
    response = client.responses.create(
        model=req.model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": req.prompt},
                    {"type": "input_image", "image_url": image_data_url(req.image_path)},
                ],
            }
        ],
        max_output_tokens=req.max_tokens,
    )
    text = getattr(response, "output_text", "") or ""
    return VisionResponse(text=text, raw=response.model_dump())
