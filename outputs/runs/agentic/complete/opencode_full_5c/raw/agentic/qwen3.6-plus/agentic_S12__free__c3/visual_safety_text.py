from __future__ import annotations

from vision_client import (
    get_openai_client,
    build_vision_messages,
    call_vision_api,
    DEFAULT_TEXT_MODEL,
)
from detect_image_labels import detect_image_labels
from detect_image_text import detect_image_text
from vision_models import ImageLabelResponse, ImageTextResponse


TEXT_SAFETY_SYSTEM_PROMPT = (
    "You are a text-safety classifier powered by the OpenAI gpt-4o model. "
    "Analyze the provided image labels and detected text for unsafe, offensive, "
    "or policy-violating content. Return a JSON object with: "
    "'text_safe' (boolean), 'labels_safe' (boolean), "
    "'flagged_items' (list of strings that triggered flags), "
    "'reasons' (list of explanation strings), and "
    "'overall_safe' (boolean, true only if both text and labels are safe). "
    "Return only valid JSON with no extra text."
)

TEXT_SAFETY_USER_PROMPT = (
    "Review the following extracted content from an image for unsafe text:\n\n"
    "Detected Labels: {labels}\n"
    "Detected Text: {text}\n\n"
    "Flag any content that is offensive, hateful, explicit, or policy-violating."
)


def check_visual_safety_text(
    labels: list[str] | None = None,
    detected_text: str | None = None,
    model: str = DEFAULT_TEXT_MODEL,
) -> dict:
    labels_str = ", ".join(labels) if labels else "(none)"
    text_str = detected_text or "(none)"

    user_prompt = TEXT_SAFETY_USER_PROMPT.format(
        labels=labels_str,
        text=text_str,
    )
    messages = build_vision_messages(
        system_prompt=TEXT_SAFETY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_path=None,
    )
    raw = call_vision_api(messages, model=model)
    import json

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {
            "text_safe": True,
            "labels_safe": True,
            "flagged_items": [],
            "reasons": ["Failed to parse safety response"],
            "overall_safe": False,
        }
    return result


def check_image_text_safety(
    image_path: str,
    model: str = DEFAULT_TEXT_MODEL,
) -> dict:
    labels_resp = detect_image_labels(image_path)
    text_resp = detect_image_text(image_path)

    label_names = [l.name for l in labels_resp.labels]
    result = check_visual_safety_text(
        labels=label_names,
        detected_text=text_resp.full_text,
        model=model,
    )
    result["image_path"] = image_path
    return result


def check_text_safety_batch(
    label_text_pairs: list[tuple[list[str], str]],
    model: str = DEFAULT_TEXT_MODEL,
) -> list[dict]:
    results: list[dict] = []
    for labels, text in label_text_pairs:
        result = check_visual_safety_text(
            labels=labels,
            detected_text=text,
            model=model,
        )
        results.append(result)
    return results


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    result = check_image_text_safety(path)
    print(f"Overall safe: {result.get('overall_safe')}")
    print(f"Flagged: {result.get('flagged_items')}")
    print(f"Reasons: {result.get('reasons')}")
