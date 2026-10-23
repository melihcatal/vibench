from vision_client import azure_vision_endpoint, post_json
from vision_models import VisionImageInput, build_response, normalize_text_items


def detect_image_labels(image: VisionImageInput):
    url = azure_vision_endpoint(
        "/computervision/imageanalysis:analyze?api-version=2024-02-01&features=tags"
    )
    payload = (
        {"url": image.url}
        if image.url
        else {"base64Source": __import__("vision_client").encode_image_base64(image)}
    )
    raw = post_json(url, payload)
    labels = [
        item.get("name", "") for item in raw.get("tagsResult", {}).get("values", [])
    ]
    return build_response("azure-ai-vision", raw, labels=normalize_text_items(labels))
