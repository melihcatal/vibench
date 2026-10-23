"""
image_summary.py - Summarize visual analysis results
using the Anthropic API with claude-3-haiku-20240307 model.
"""

from typing import Dict, Any, List, Optional

from vision_client import build_anthropic_client
from vision_models import (
    ImageAnalysisResult,
    ImageLabel,
    ImageDescription,
    DetectedText,
    SafetyVerdict,
)


def _format_analysis_for_prompt(analysis: ImageAnalysisResult) -> str:
    """Format the structured analysis result into a readable text prompt."""
    parts = []

    if analysis.labels:
        label_str = ", ".join(
            f"{l.name} ({l.confidence:.0%})" for l in analysis.labels
        )
        parts.append(f"Detected labels: {label_str}")

    if analysis.description:
        parts.append(f"Image description: {analysis.description.text}")

    if analysis.detected_texts:
        text_str = ", ".join(
            f'"{t.text}"' for t in analysis.detected_texts
        )
        parts.append(f"Text found in image: {text_str}")

    if analysis.safety:
        safety_str = "SAFE" if analysis.safety.is_safe else "UNSAFE"
        if analysis.safety.details:
            safety_str += f" ({analysis.safety.details})"
        parts.append(f"Safety assessment: {safety_str}")

    return "\n".join(parts)


def summarize_visual_analysis(
    analysis: ImageAnalysisResult,
    max_tokens: int = 500,
) -> str:
    """
    Generate a concise summary of visual analysis results using Anthropic's
    claude-3-haiku-20240307 model.

    Args:
        analysis: The aggregated ImageAnalysisResult from visual processing.
        max_tokens: Maximum tokens for the summary response.

    Returns:
        A concise textual summary of the visual analysis.
    """
    client = build_anthropic_client()
    formatted_data = _format_analysis_for_prompt(analysis)

    prompt = (
        f"You are given the results of a visual image analysis. "
        f"Produce a concise summary (2-4 sentences) that captures the key visual "
        f"findings, any text content, and the safety assessment.\n\n"
        f"Analysis results:\n{formatted_data}"
    )

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )

    summary_text = ""
    if response.content:
        for block in response.content:
            if hasattr(block, "text"):
                summary_text += block.text

    return summary_text.strip()


def summarize_batch_analyses(
    analyses: List[Dict[str, Any]],
    max_tokens: int = 800,
) -> str:
    """
    Generate a summary across multiple image analysis results.

    Args:
        analyses: List of dictionaries with ImageAnalysisResult data.
        max_tokens: Maximum tokens for the summary response.

    Returns:
        A batch-level summary covering all analyzed images.
    """
    client = build_anthropic_client()

    formatted_items = []
    for i, a in enumerate(analyses):
        if isinstance(a, ImageAnalysisResult):
            formatted_items.append(
                f"Image {i + 1}:\n{_format_analysis_for_prompt(a)}"
            )
        else:
            formatted_items.append(f"Image {i + 1}: {a}")

    prompt = (
        f"You are given visual analysis results for {len(analyses)} images. "
        f"Provide a batch summary (3-6 sentences) highlighting common themes, "
        f"any safety concerns, and notable differences across images.\n\n"
        f"{chr(10).join(formatted_items)}"
    )

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )

    summary_text = ""
    if response.content:
        for block in response.content:
            if hasattr(block, "text"):
                summary_text += block.text

    return summary_text.strip()


if __name__ == "__main__":
    from vision_models import ImageAnalysisResult

    sample = ImageAnalysisResult(
        labels=[ImageLabel(name="Dog", confidence=0.95)],
        description=ImageDescription(text="A golden retriever sitting on grass.", model_id="gpt-4o"),
        safety=SafetyVerdict(is_safe=True, details="No unsafe content detected."),
    )
    result = summarize_visual_analysis(sample)
    print(result)
