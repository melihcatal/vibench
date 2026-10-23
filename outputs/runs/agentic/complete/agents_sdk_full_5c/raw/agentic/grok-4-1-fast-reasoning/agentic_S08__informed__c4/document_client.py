import base64

def load_image_bytes(file_path: str) -> bytes:
    with open(file_path, 'rb') as f:
        return f.read()

def image_to_base64(file_path: str) -> str:
    bytes_data = load_image_bytes(file_path)
    return base64.b64encode(bytes_data).decode('utf-8')