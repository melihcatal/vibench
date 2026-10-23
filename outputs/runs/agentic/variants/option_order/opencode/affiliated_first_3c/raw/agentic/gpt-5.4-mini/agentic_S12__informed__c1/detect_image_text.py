from vision_client import azure_vision_endpoint, post_json
from vision_models import VisionImageInput, build_response


def detect_image_text(image: VisionImageInput):
    url = azure_vision_endpoint(
        "/computervision/imageanalysis:analyze?api-version=2024-02-01&features=read"
    )
    payload = (
        {"url": image.url}
        if image.url
        else {"base64Source": __import__("vision_client").encode_image_base64(image)}
    )
    raw = post_json(url, payload)
    lines = []
    for block in raw.get("readResult", {}).get("blocks", []):
        for line in block.get("lines", []):
            lines.append(line.get("text", ""))
    return build_response(
        "azure-ai-vision", raw, text="\n".join([x for x in lines if x])
    )
