from google.cloud import vision


def describe_image(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    response = client.image_properties(
        image=vision.Image(content=payload["image_bytes"]),
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    descriptions = []
    for prop in response.image_properties_annotation.dominant_colors.colors[: int(config.get("max_descriptions", 1))]:
        descriptions.append({"description": f"Image with dominant color {prop.color.red},{prop.color.green},{prop.color.blue}", "confidence": prop.score})
    return {"descriptions": descriptions}
