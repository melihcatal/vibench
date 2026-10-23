import os
import json
from typing import Optional, List
from dashscope import Generation
from vision_models import LabelDetectionResponse, ImageDescriptionResponse


DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "")


def summarize_visual_analysis(
    labels_response: Optional[LabelDetectionResponse] = None,
    description_response: Optional[ImageDescriptionResponse] = None,
    text_response: Optional[object] = None,
    max_tokens: int = 256,
) -> str:
    sections = []
    if description_response and description_response.description:
        sections.append(f"Description: {description_response.description}")
    if labels_response and labels_response.labels:
        top_labels = sorted(
            labels_response.labels, key=lambda l: l.confidence, reverse=True
        )[:5]
        label_str = ", ".join(
            f"{lbl.name} ({lbl.confidence:.0f}%)" for lbl in top_labels
        )
        sections.append(f"Top labels: {label_str}")
    if (
        text_response
        and hasattr(text_response, "full_text")
        and text_response.full_text
    ):
        sections.append(f"Detected text: {text_response.full_text}")
    if not sections:
        return "No visual analysis data available."
    prompt = (
        "Summarize the following visual analysis of an image into a concise, coherent paragraph. "
        "Focus on the most important visual elements and their significance.\n\n"
        + "\n".join(sections)
    )
    response = Generation.call(
        api_key=DASHSCOPE_API_KEY,
        model="qwen-turbo",
        prompt=prompt,
        max_tokens=max_tokens,
        result_format="message",
    )
    if (
        response.status_code == 200
        and response.output
        and response.output.get("choices")
    ):
        return response.output["choices"][0]["message"]["content"]
    return "Summary generation failed."


if __name__ == "__main__":
    summary = summarize_visual_analysis()
    print(summary)
