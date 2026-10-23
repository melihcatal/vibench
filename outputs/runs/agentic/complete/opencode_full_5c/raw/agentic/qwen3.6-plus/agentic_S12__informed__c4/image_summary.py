import os
import json
from typing import Optional

import anthropic
from anthropic import Anthropic

from vision_models import (
    ImageSummaryRequest,
    ImageSummaryResponse,
    DetectedLabel,
    SafetyScoreResponse,
)


ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-20250514")


def build_summary_prompt(request: ImageSummaryRequest) -> str:
    label_list = ", ".join(
        f"{l.name} ({l.confidence:.1f}%)" for l in request.labels[:15]
    )

    text_list = (
        ", ".join(request.detected_texts[:10]) if request.detected_texts else "none"
    )

    safety_info = "No safety analysis available."
    if request.safety_result:
        if request.safety_result.is_safe:
            safety_info = "Image passed safety checks."
        else:
            flagged = [
                c.name
                for c in request.safety_result.categories
                if c.confidence >= request.safety_result.threshold * 100
            ]
            safety_info = f"Safety concerns detected: {', '.join(flagged)}."

    prompt = (
        f"Provide a concise 2-3 sentence summary of this image based on the following analysis:\n\n"
        f"Detected labels: {label_list}\n"
        f"Description: {request.description}\n"
        f"Text found in image: {text_list}\n"
        f"Safety: {safety_info}\n\n"
        f"Write a clear, informative summary suitable for accessibility purposes."
    )
    return prompt


def summarize_visual_analysis(
    request: ImageSummaryRequest, model: str = CLAUDE_MODEL
) -> ImageSummaryResponse:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = build_summary_prompt(request)

    message = client.messages.create(
        model=model,
        max_tokens=300,
        system="You are an expert at summarizing visual analysis results into clear, accessible descriptions.",
        messages=[{"role": "user", "content": prompt}],
    )

    summary = message.content[0].text.strip()

    return ImageSummaryResponse(
        summary=summary,
        model=f"anthropic-{model}",
    )


def summarize_from_results(
    labels: list,
    description: str,
    detected_texts: list,
    safety_result: Optional[SafetyScoreResponse] = None,
    model: str = CLAUDE_MODEL,
) -> ImageSummaryResponse:
    request = ImageSummaryRequest(
        labels=labels,
        description=description,
        detected_texts=detected_texts,
        safety_result=safety_result,
    )
    return summarize_visual_analysis(request, model=model)
