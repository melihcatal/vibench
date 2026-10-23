import base64
import json
from urllib import request

from vision_client import build_headers, load_config
from vision_models import make_result


def describe_image(image_path: str):
    config = load_config()
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")
    payload = json.dumps(
        {
            "model": config.model,
            "input": {
                "image": f"data:image/jpeg;base64,{image_b64}",
                "task": "caption",
            },
        }
    ).encode("utf-8")
    req = request.Request(
        config.base_url, data=payload, headers=build_headers(config), method="POST"
    )
    with request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return make_result(
        text=data.get("output", {}).get("caption", ""),
        labels=[],
        unsafe=False,
        provider="dashscope",
    )
