import google.generativeai as genai
import json
from typing import Dict, Any


def upload_image(image_path: str) -> genai.File:
    return genai.upload_file(image_path, timeout=20.0)


def parse_vision_response(response: genai.protos.Content) -> Dict[str, Any]:
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"raw_response": response.text, "parse_error": "Invalid JSON from model"}
