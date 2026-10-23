from __future__ import annotations

from vision_client import azure_vision_analyze
from vision_models import ImageSource, TextDetectionResult, flatten_text_lines


def detect_image_text(image: ImageSource) -> TextDetectionResult:
    response = azure_vision_analyze(image, features="read")
    blocks = response.get("readResult", {}).get("blocks", [])
    lines = []
    for block in blocks:
        for line in block.get("lines", []):
            text = line.get("text", "").strip()
            if text:
                lines.append(text)
    full_text = "\n".join(lines)
    return TextDetectionResult(
        provider="azure_ai_vision",
        text=full_text,
        lines=flatten_text_lines(full_text),
        raw_response=response,
    )
