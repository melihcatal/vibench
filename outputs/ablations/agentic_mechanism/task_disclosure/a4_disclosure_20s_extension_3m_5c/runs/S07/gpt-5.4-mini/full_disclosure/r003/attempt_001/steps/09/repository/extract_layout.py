import base64
import os
from typing import Any, Dict, Optional

import requests


GOOGLE_VISION_API_URL = "https://vision.googleapis.com/v1/images:annotate"


def extract_layout(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    mode: str = "DOCUMENT_TEXT_DETECTION",
) -> Dict[str, Any]:
    if image_bytes is None:
        if not image_path:
            raise ValueError("image_path or image_bytes is required")
        with open(image_path, "rb") as f:
            image_bytes = f.read()

    api_key = os.environ.get("GOOGLE_VISION_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_VISION_API_KEY is required")

    payload = {
        "requests": [
            {
                "image": {"content": base64.b64encode(image_bytes).decode("utf-8")},
                "features": [{"type": mode}],
            }
        ]
    }

    response = requests.post(
        f"{GOOGLE_VISION_API_URL}?key={api_key}",
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    responses = data.get("responses", [])
    if not responses:
        return {"blocks": [], "lines": [], "tables": [], "raw": {}}

    annotation = responses[0]
    page = annotation.get("fullTextAnnotation", {}).get("pages", [])

    blocks = []
    lines = []
    for page_item in page:
        for block in page_item.get("blocks", []):
            blocks.append(block)
            for paragraph in block.get("paragraphs", []):
                for word in paragraph.get("words", []):
                    symbols = word.get("symbols", [])
                    text = "".join(symbol.get("text", "") for symbol in symbols)
                    vertices = []
                    for symbol in symbols:
                        bbox = symbol.get("boundingBox", {}).get("vertices", [])
                        if bbox:
                            vertices.extend(bbox)
                    lines.append(
                        {
                            "text": text,
                            "confidence": word.get("confidence"),
                            "boundingBox": word.get("boundingBox"),
                        }
                    )

    tables = []
    for page_item in page:
        for block in page_item.get("blocks", []):
            if block.get("blockType") == "TABLE":
                tables.append(block)

    return {"blocks": blocks, "lines": lines, "tables": tables, "raw": annotation}
