import base64
import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class VisionConfig:
    api_key: str
    api_base: str
    model: str


def get_openai_vision_config() -> VisionConfig:
    return VisionConfig(
        api_key=os.environ['OPENAI_API_KEY'],
        api_base=os.getenv('OPENAI_API_BASE', 'https://api.openai.com/v1'),
        model=os.getenv('OPENAI_VISION_MODEL', 'gpt-4.1-mini'),
    )


def image_source_to_data_url(image_path: str) -> str:
    path = Path(image_path)
    mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    data = path.read_bytes()
    encoded = base64.b64encode(data).decode('ascii')
    return f'data:{mime};base64,{encoded}'
