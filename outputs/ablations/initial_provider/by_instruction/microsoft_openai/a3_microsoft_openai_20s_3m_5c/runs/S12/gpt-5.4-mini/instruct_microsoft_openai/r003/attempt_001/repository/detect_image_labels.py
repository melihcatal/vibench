from vision_client import get_client, image_data_url, load_vision_config
from vision_models import build_result


def detect_image_labels(image_path: str):
    cfg = load_vision_config()
    client = get_client(cfg)
    resp = client.responses.create(
        model=cfg.model,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": "Identify the main objects and labels visible in this image. Return a concise list."},
                    {"type": "input_image", "image_url": image_data_url(image_path)},
                ],
            }
        ],
    )
    text = getattr(resp, "output_text", "") or ""
    return build_result(text=text, items=text, raw=resp.model_dump() if hasattr(resp, "model_dump") else None)
