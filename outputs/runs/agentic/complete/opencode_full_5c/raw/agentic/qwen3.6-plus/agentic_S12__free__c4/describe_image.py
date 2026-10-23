from vision_client import (
    get_vision_client,
    build_vision_payload,
    parse_vision_response,
    VISION_MODEL,
)
from vision_models import ImageDescription, normalize_description

VISION_MODEL_ID = "gpt-4o"

PROMPT_TEMPLATE = (
    "Provide a concise visual description of the image in 2-3 sentences. "
    "Describe the main subjects, setting, colors, and notable visual details. "
    "Keep the description objective and factual."
)


def describe_image(image_url: str = None, image_base64: str = None) -> ImageDescription:
    client = get_vision_client()
    payload = build_vision_payload(
        image_url=image_url,
        image_base64=image_base64,
        prompt=PROMPT_TEMPLATE,
    )
    response = client.chat.completions.create(**payload)
    raw_text = parse_vision_response(response)
    description = normalize_description(raw_text)
    return description


if __name__ == "__main__":
    import sys

    image_source = sys.argv[1] if len(sys.argv) > 1 else None
    if image_source and image_source.startswith("http"):
        result = describe_image(image_url=image_source)
    elif image_source:
        import base64

        with open(image_source, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        result = describe_image(image_base64=b64)
    else:
        raise ValueError("Provide image URL or file path")
    print(result.description)
