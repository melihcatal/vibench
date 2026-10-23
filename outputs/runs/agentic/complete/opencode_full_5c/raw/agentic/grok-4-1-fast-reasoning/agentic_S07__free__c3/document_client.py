def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as f:
        return f.read()
