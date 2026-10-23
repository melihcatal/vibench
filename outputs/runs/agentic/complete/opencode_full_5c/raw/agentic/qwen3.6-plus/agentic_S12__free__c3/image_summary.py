from __future__ import annotations

from vision_client import (
    get_openai_client,
    build_vision_messages,
    call_vision_api,
    DEFAULT_TEXT_MODEL,
)
from vision_models import (
    ImageLabelResponse,
    ImageDescriptionResponse,
    ImageTextResponse,
    ImageSafetyResponse,
)

from detect_image_labels import detect_image_labels
from describe_image import describe_image
from detect_image_text import detect_image_text
from score_image_safety import score_image_safety


SUMMARIZE_SYSTEM_PROMPT = (
    "You are a visual-analysis summarizer powered by the OpenAI gpt-4o model. "
    "Combine the provided image analysis results into a concise, coherent summary. "
    "Include key labels, a brief description, any detected text, and safety assessment. "
    "Keep the summary under 250 words."
)

SUMMARIZE_USER_PROMPT = (
    "Summarize the following visual analysis results for the image:\n\n"
    "Labels: {labels}\n"
    "Description: {description}\n"
    "Detected Text: {text}\n"
    "Safety: {safety}\n\n"
    "Produce a unified summary."
)


def summarize_visual_analysis(
    image_path: str,
    labels_resp: ImageLabelResponse | None = None,
    description_resp: ImageDescriptionResponse | None = None,
    text_resp: ImageTextResponse | None = None,
    safety_resp: ImageSafetyResponse | None = None,
    model: str = DEFAULT_TEXT_MODEL,
) -> str:
    if labels_resp is None:
        labels_resp = detect_image_labels(image_path)
    if description_resp is None:
        description_resp = describe_image(image_path)
    if text_resp is None:
        text_resp = detect_image_text(image_path)
    if safety_resp is None:
        safety_resp = score_image_safety(image_path)

    labels_str = ", ".join(f"{l.name} ({l.confidence:.2f})" for l in labels_resp.labels)
    description_str = description_resp.description
    text_str = text_resp.full_text or "(none)"
    safety_str = f"safe={safety_resp.overall_safe}, " + ", ".join(
        f"{s.category}={s.score:.2f}" for s in safety_resp.scores
    )

    user_prompt = SUMMARIZE_USER_PROMPT.format(
        labels=labels_str,
        description=description_str,
        text=text_str,
        safety=safety_str,
    )
    messages = build_vision_messages(
        system_prompt=SUMMARIZE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        image_path=None,
    )
    return call_vision_api(messages, model=model)


def summarize_image_full(
    image_path: str,
    model: str = DEFAULT_TEXT_MODEL,
) -> dict:
    labels_resp = detect_image_labels(image_path)
    description_resp = describe_image(image_path)
    text_resp = detect_image_text(image_path)
    safety_resp = score_image_safety(image_path)
    summary = summarize_visual_analysis(
        image_path=image_path,
        labels_resp=labels_resp,
        description_resp=description_resp,
        text_resp=text_resp,
        safety_resp=safety_resp,
        model=model,
    )
    return {
        "image_path": image_path,
        "labels": labels_resp,
        "description": description_resp,
        "text": text_resp,
        "safety": safety_resp,
        "summary": summary,
    }


if __name__ == "__main__":
    import sys

    path = sys.argv[1] if len(sys.argv) > 1 else "sample.jpg"
    result = summarize_image_full(path)
    print(result["summary"])
