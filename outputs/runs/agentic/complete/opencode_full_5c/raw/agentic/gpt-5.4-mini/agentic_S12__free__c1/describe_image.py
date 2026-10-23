from vision_client import extract_response_text, openai_vision_request


def describe_image(image_path: str) -> str:
    data = openai_vision_request(
        "Write one short visual description of this image.", image_path
    )
    return extract_response_text(data).strip()
