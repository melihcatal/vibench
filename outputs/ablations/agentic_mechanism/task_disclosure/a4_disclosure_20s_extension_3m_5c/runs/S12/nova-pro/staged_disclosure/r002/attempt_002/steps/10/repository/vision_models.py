def request_static_image(image_path: str) -> dict:
    return {"image_path": image_path}

def request_visual_understanding(image_path: str) -> dict:
    return {"image_path": image_path}

def normalize_response(response: dict) -> dict:
    return response

def normalize_image(image_path: str) -> str:
    return image_path