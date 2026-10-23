from vision_client import extract_response_text, openai_vision_request


def detect_image_text(image_path: str) -> str:
    data = openai_vision_request(
        "Extract all readable text from this image, preserving line breaks.", image_path
    )
    return extract_response_text(data).strip()
