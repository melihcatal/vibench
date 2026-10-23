import base64


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def image_to_base64(image_path: str) -> str:
    bytes_data = load_image_bytes(image_path)
    return base64.b64encode(bytes_data).decode("utf-8")
