import base64
import os
from dataclasses import dataclass


def load_vision_config(config=None):
    config = dict(config or {})
    config.setdefault("aws_region", os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))
    config.setdefault("aws_max_labels", int(os.getenv("AWS_MAX_LABELS", "10")))
    config.setdefault("aws_max_text_detections", int(os.getenv("AWS_MAX_TEXT_DETECTIONS", "10")))
    config.setdefault("aws_min_confidence", float(os.getenv("AWS_MIN_CONFIDENCE", "0")))
    config.setdefault("aws_image_format", os.getenv("AWS_IMAGE_FORMAT", "bytes"))
    config.setdefault("openai_model", os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"))
    config.setdefault("openai_api_key", os.getenv("OPENAI_API_KEY"))
    config.setdefault("openai_base_url", os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    config.setdefault("s3_bucket", os.getenv("AWS_S3_BUCKET"))
    config.setdefault("s3_prefix", os.getenv("AWS_S3_PREFIX", "image-archive/"))
    config.setdefault("target_language", os.getenv("TARGET_LANGUAGE", "es"))
    return config


def image_bytes_from_payload(payload):
    if isinstance(payload, dict):
        if "image_bytes" in payload:
            return payload["image_bytes"]
        if "image_base64" in payload:
            return base64.b64decode(payload["image_base64"])
        if "image_path" in payload:
            with open(payload["image_path"], "rb") as f:
                return f.read()
    return payload


@dataclass
class OpenAIImageClient:
    api_key: str
    base_url: str
    model: str

    def headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
