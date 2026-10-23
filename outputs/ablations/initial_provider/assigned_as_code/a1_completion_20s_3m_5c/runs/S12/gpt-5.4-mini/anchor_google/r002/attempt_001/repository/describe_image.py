from google.cloud import vision


def describe_image(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    response = client.annotate_image(
        image=vision.Image(content=payload["image_bytes"]),
        features=[vision.Feature(type_=vision.Feature.Type.DESCRIPTION)]
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    annotations = getattr(response, "localized_object_annotations", None) or []
    if annotations:
        top = annotations[0]
        return {"description": top.name, "confidence": top.score}
    descriptions = getattr(response, "text_annotations", None) or []
    return {"description": descriptions[0].description if descriptions else "", "confidence": 0.0}
