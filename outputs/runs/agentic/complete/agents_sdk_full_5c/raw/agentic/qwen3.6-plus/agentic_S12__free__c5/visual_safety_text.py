"""
visual_safety_text.py - Check generated visual labels for unsafe text
using the Anthropic API with claude-3-haiku-20240307 model.
"""

from typing import List, Optional

from vision_client import build_anthropic_client
from vision_models import (
    SafetyTextVerdict,
    ImageLabel,
    DetectedText,
    ImageDescription,
)


def check_visual_labels_text(
    labels: List[ImageLabel],
    detected_texts: List[DetectedText],
    description: Optional[ImageDescription] = None,
) -> SafetyTextVerdict:
    """
    Check the textual output of image analysis (labels, detected text, and
    descriptions) for unsafe or policy-sensitive content using the Anthropic
    claude-3-haiku-20240307 model.

    Args:
        labels: List of ImageLabel objects detected in the image.
        detected_texts: List of DetectedText objects from OCR.
        description: Optional ImageDescription for the image.

    Returns:
        SafetyTextVerdict with safety assessment details.
    """
    client = build_anthropic_client()

    label_strs = [f"{l.name} ({l.confidence:.0%})" for l in labels]
    text_strs = [f'"{t.text}" ({t.confidence:.0%})' for t in detected_texts]
    desc_str = description.text if description else "No description available."

    content_block = (
        "Analyze the following text extracted from an image analysis pipeline "
        "and determine if any labels, OCR text, or descriptions contain unsafe, "
        "offensive, or policy-violating content. Categories to flag include: "
        "hate speech, explicit content, harassment, self-harm, illegal activity, "
        "or personally identifiable information.\n\n"
        f"Detected labels: {', '.join(label_strs) if label_strs else 'None'}\n"
        f"Detected text: {', '.join(text_strs) if text_strs else 'None'}\n"
        f"Image description: {desc_str}\n\n"
        "Respond in this exact format:\n"
        "SAFE: true/false\n"
        "FLAGS: comma-separated list of flagged categories or NONE\n"
        "DETAILS: brief explanation\n"
    )

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[{"role": "user", "content": content_block}],
    )

    result_text = ""
    if response.content:
        for block in response.content:
            if hasattr(block, "text"):
                result_text += block.text

    result_text = result_text.strip()
    is_safe = True
    flags = []
    details = None

    for line in result_text.split("\n"):
        line_lower = line.lower().strip()
        if line_lower.startswith("safe:"):
            is_safe = line_lower.split(":", 1)[1].strip() not in ("true",)
            is_safe = line_lower.split(":", 1)[1].strip().lower() != "true"
        elif line_lower.startswith("flags:"):
            flag_str = line.split(":", 1)[1].strip()
            if flag_str.upper() != "NONE":
                flags = [f.strip() for f in flag_str.split(",") if f.strip()]
        elif line_lower.startswith("details:"):
            details = line.split(":", 1)[1].strip()

    if not details and result_text:
        details = result_text

    return SafetyTextVerdict(
        is_safe=is_safe,
        flags=flags,
        details=details,
    )


def check_description_text(
    description: ImageDescription,
) -> SafetyTextVerdict:
    """
    Check a single image description for unsafe text content.

    Args:
        description: An ImageDescription object to check.

    Returns:
        SafetyTextVerdict with safety assessment.
    """
    return check_visual_labels_text(
        labels=[],
        detected_texts=[],
        description=description,
    )


if __name__ == "__main__":
    sample_labels = [
        ImageLabel(name="Person", confidence=0.92),
        ImageLabel(name="Beach", confidence=0.88),
    ]
    sample_texts = [
        DetectedText(text="Welcome to Paradise Beach", confidence=0.95),
    ]
    sample_desc = ImageDescription(
        text="A person relaxing on a sunny beach with clear skies.",
        model_id="gpt-4o",
    )

    result = check_visual_labels_text(sample_labels, sample_texts, sample_desc)
    print(f"Safe: {result.is_safe}")
    print(f"Flags: {result.flags}")
    print(f"Details: {result.details}")
