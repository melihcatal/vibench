from vision_client import azure_vision_endpoint, post_json
from vision_models import VisionImageInput, build_response


def score_image_safety(image: VisionImageInput):
    url = azure_vision_endpoint(
        "/computervision/imageanalysis:analyze?api-version=2024-02-01&features=adult"
    )
    payload = (
        {"url": image.url}
        if image.url
        else {"base64Source": __import__("vision_client").encode_image_base64(image)}
    )
    raw = post_json(url, payload)
    adult = raw.get("adultResult", {})
    unsafe = any(
        bool(adult.get(key))
        for key in ("isAdultContent", "isGoryContent", "isRacyContent")
    )
    return build_response("azure-ai-vision", raw, unsafe=unsafe)
