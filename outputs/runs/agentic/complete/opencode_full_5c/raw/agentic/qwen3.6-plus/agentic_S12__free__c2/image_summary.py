import os
import json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict

from detect_image_labels import detect_image_labels, ImageLabelResponse
from describe_image import describe_image, ImageDescriptionResponse
from detect_image_text import detect_image_text, ImageTextResponse
from score_image_safety import score_image_safety, ImageSafetyResponse


@dataclass
class VisualAnalysisSummary:
    image_path: str
    label_count: int
    top_labels: List[str]
    description_count: int
    descriptions: List[str]
    text_detected: bool
    text_snippet: str
    is_safe: bool
    safety_score: float
    unsafe_flags: List[str]
    model_providers: Dict[str, str]


def summarize_visual_analysis(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    include_text: bool = True,
    include_safety: bool = True,
) -> VisualAnalysisSummary:
    if image_path is None and image_bytes is None:
        raise ValueError("Either image_path or image_bytes must be provided")

    source = image_path or "<bytes>"

    labels_result = detect_image_labels(
        image_path=image_path,
        image_bytes=image_bytes,
        max_labels=10,
    )

    description_result = describe_image(
        image_path=image_path,
        image_bytes=image_bytes,
        max_descriptions=3,
    )

    text_result = None
    if include_text:
        text_result = detect_image_text(
            image_path=image_path,
            image_bytes=image_bytes,
        )

    safety_result = None
    if include_safety:
        safety_result = score_image_safety(
            image_path=image_path,
            image_bytes=image_bytes,
        )

    top_labels = [lbl.name for lbl in labels_result.labels[:5]]
    text_detected = text_result is not None and bool(text_result.full_text.strip())
    text_snippet = ""
    if text_result and text_result.full_text:
        text_snippet = text_result.full_text[:200]

    is_safe = True
    safety_score = 100.0
    unsafe_flags = []
    if safety_result:
        is_safe = safety_result.is_safe
        safety_score = safety_result.safety_score
        unsafe_flags = [det.name for det in safety_result.unsafe_detections]

    model_providers = {
        "labels": labels_result.label_model,
        "description": description_result.model,
        "text": text_result.model if text_result else "skipped",
        "safety": safety_result.model if safety_result else "skipped",
    }

    summary = VisualAnalysisSummary(
        image_path=source,
        label_count=len(labels_result.labels),
        top_labels=top_labels,
        description_count=len(description_result.descriptions),
        descriptions=description_result.descriptions,
        text_detected=text_detected,
        text_snippet=text_snippet,
        is_safe=is_safe,
        safety_score=safety_score,
        unsafe_flags=unsafe_flags,
        model_providers=model_providers,
    )

    return summary


def format_summary_report(summary: VisualAnalysisSummary) -> str:
    lines = [
        f"Visual Analysis Summary for: {summary.image_path}",
        f"Labels detected: {summary.label_count}",
        f"Top labels: {', '.join(summary.top_labels)}",
        f"Descriptions: {summary.description_count}",
    ]
    for desc in summary.descriptions:
        lines.append(f"  - {desc}")
    lines.append(f"Text detected: {summary.text_detected}")
    if summary.text_snippet:
        lines.append(f"Text snippet: {summary.text_snippet}")
    lines.append(f"Image safe: {summary.is_safe}")
    lines.append(f"Safety score: {summary.safety_score:.1f}")
    if summary.unsafe_flags:
        lines.append(f"Unsafe flags: {', '.join(summary.unsafe_flags)}")
    lines.append(f"Models used: {json.dumps(summary.model_providers, indent=2)}")
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python image_summary.py <image_path>")
        sys.exit(1)

    summary = summarize_visual_analysis(image_path=sys.argv[1])
    print(format_summary_report(summary))
