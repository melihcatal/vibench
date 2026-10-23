import re

from vision_models import VisionResult


def visual_safety_text(text_items):
    blocked = [item for item in text_items if re.search(r"(?i)weapon|blood|nsfw|explicit", str(item))]
    return VisionResult(provider="local.regex", kind="text_safety", source="generated_labels", data={"unsafe": bool(blocked), "matches": blocked})
