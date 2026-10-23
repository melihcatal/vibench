"""
image_summary.py - Summarize visual analysis results using Qwen
via DashScope multimodal language model.

Provider: Qwen via DashScope
SDK: dashscope
Auth: DASHSCOPE_API_KEY
Model: qwen-vl-plus
"""

import os
import sys
import json
from typing import Optional, List, Dict, Any

import dashscope
from dashscope import MultiModalConversation


def summarize_visual_results(
    labels: Optional[List[Dict[str, Any]]] = None,
    description: Optional[str] = None,
    detected_text: Optional[str] = None,
    safety_assessment: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Generate a concise summary of visual analysis results
    using Qwen-VL model on DashScope.

    Args:
        labels: List of detected label dicts with 'name' and 'confidence'.
        description: Visual description string of the image.
        detected_text: Any text detected within the image.
        safety_assessment: Safety assessment dict from score_image_safety.

    Returns:
        A human-readable summary string of the visual analysis.
    """
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError(
            "DASHSCOPE_API_KEY environment variable must be set "
            "for DashScope Qwen API access."
        )

    dashscope.api_key = api_key

    analysis_components = []

    if description:
        analysis_components.append(f"Visual Description: {description}")

    if labels:
        label_strs = [f"{lbl['name']} ({lbl['confidence']}%)" for lbl in labels]
        analysis_components.append(f"Detected Labels: {', '.join(label_strs)}")

    if detected_text:
        analysis_components.append(f"Detected Text: {detected_text}")

    if safety_assessment:
        safety_status = "SAFE" if safety_assessment.get("is_safe") else "FLAGGED"
        score = safety_assessment.get("safety_score", "N/A")
        analysis_components.append(
            f"Safety Assessment: {safety_status} (score: {score})"
        )

    analysis_text = "\n".join(analysis_components) if analysis_components else "No analysis data provided."

    prompt = (
        f"Below are the results from a comprehensive image analysis pipeline.\n"
        f"Please provide a concise, well-structured summary (3-5 sentences) that "
        f"synthesizes these findings into a coherent overview.\n\n"
        f"Analysis Results:\n{analysis_text}\n\n"
        f"Summary:"
    )

    messages = [
        {
            "role": "system",
            "content": "You are a visual analysis summarizer. Provide clear, concise summaries of image analysis results.",
        },
        {
            "role": "user",
            "content": [
                {"text": prompt}
            ],
        },
    ]

    response = MultiModalConversation.call(
        model="qwen-vl-plus",
        messages=messages,
    )

    if response.status_code == 200:
        summary = response.output.choices[0].message.content[0]["text"]
        return summary
    else:
        raise RuntimeError(
            f"DashScope Qwen API request failed: {response.code} - {response.message}"
        )


def summarize_from_pipeline_results(
    pipeline_output: Dict[str, Any],
) -> str:
    """
    Summarize results from a full pipeline output dict.

    Expected keys: labels, description, detected_text, safety_assessment.
    """
    return summarize_visual_results(
        labels=pipeline_output.get("labels"),
        description=pipeline_output.get("description"),
        detected_text=pipeline_output.get("detected_text"),
        safety_assessment=pipeline_output.get("safety_assessment"),
    )


def main():
    """CLI entry point for summarizing visual results from a JSON file."""
    if len(sys.argv) < 2:
        print("Usage: python image_summary.py <analysis_results.json>")
        sys.exit(1)

    results_file = sys.argv[1]
    if not os.path.exists(results_file):
        print(f"Error: Results file not found: {results_file}")
        sys.exit(1)

    with open(results_file, "r") as f:
        pipeline_output = json.load(f)

    summary = summarize_from_pipeline_results(pipeline_output)
    print(summary)


if __name__ == "__main__":
    main()
