
def create_static_image_request(image_bytes: bytes, features: list[str]) -> dict:
    """
    Creates a request payload for static image analysis.

    Args:
        image_bytes: The raw bytes of the image.
        features: A list of desired analysis features (e.g., ["LABELS", "TEXT_DETECTION"]).

    Returns:
        A dictionary representing the request payload.
    """
    return {
        "image": {"content": image_bytes.decode('latin-1')},  # Assuming base64-like encoding for simplicity
        "features": [{"type": feature} for feature in features],
    }

def normalize_vision_response(response: dict) -> dict:
    """
    Normalizes a vision model response into a more consistent format.

    Args:
        response: The raw response dictionary from a vision model.

    Returns:
        A dictionary with normalized results.
    """
    normalized_data = {}

    if "responses" in response and response["responses"]:
        first_response = response["responses"][0]

        if "labelAnnotations" in first_response:
            normalized_data["labels"] = [
                annotation["description"] for annotation in first_response["labelAnnotations"]
            ]
        if "textAnnotations" in first_response:
            normalized_data["text"] = [
                annotation["description"] for annotation in first_response["textAnnotations"]
            ]
        # Add more normalization logic for other features as needed

    return normalized_data

def preprocess_image_for_vision(image_path: str) -> bytes:
    """
    Reads an image file and returns its bytes for vision API requests.

    Args:
        image_path: The path to the image file.

    Returns:
        The raw bytes of the image.
    """
    with open(image_path, "rb") as f:
        return f.read()

