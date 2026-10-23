import base64
import os

from google.cloud import vision_v1
from google.cloud.vision_v1 import types as vision_types


def get_google_credentials_path() -> str:
    return os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")


def ensure_credentials() -> None:
    cred_path = get_google_credentials_path()
    if not cred_path or not os.path.isfile(cred_path):
        raise RuntimeError(
            "GOOGLE_APPLICATION_CREDENTIALS must point to a valid service-account JSON file"
        )


def create_vision_client() -> vision_v1.ImageAnnotatorClient:
    ensure_credentials()
    return vision_v1.ImageAnnotatorClient()


def load_image_bytes(image_path: str) -> bytes:
    with open(image_path, "rb") as fh:
        return fh.read()


def image_bytes_to_content(image_bytes: bytes) -> vision_types.Image:
    return vision_types.Image(content=image_bytes)


def image_path_to_content(image_path: str) -> vision_types.Image:
    raw = load_image_bytes(image_path)
    return image_bytes_to_content(raw)


def image_bytes_to_base64(image_bytes: bytes) -> str:
    return base64.b64encode(image_bytes).decode("utf-8")


def build_image_source_from_bytes(image_bytes: bytes) -> dict:
    return {"content": image_bytes_to_base64(image_bytes)}


def build_image_source_from_path(image_path: str) -> dict:
    return {"content": image_bytes_to_base64(load_image_bytes(image_path))}
