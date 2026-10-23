import base64


def get_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()


def get_base64_image(image_path: str) -> str:
    return base64.b64encode(get_image_bytes(image_path)).decode("utf-8")
