import os

def load_image(image_path: str) -> bytes:
    with open(image_path, 'rb') as f:
        return f.read()

def get_mimetype(image_path: str) -> str:
    ext = os.path.splitext(image_path)[1].lower()
    if ext in ['.jpg', '.jpeg']:
        return 'image/jpeg'
    elif ext == '.png':
        return 'image/png'
    elif ext == '.tiff':
        return 'image/tiff'
    elif ext == '.pdf':
        return 'application/pdf'
    else:
        raise ValueError(f"Unsupported file type: {ext}")
