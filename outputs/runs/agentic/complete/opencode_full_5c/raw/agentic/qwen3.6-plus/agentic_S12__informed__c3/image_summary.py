import os

from mistralai import Mistral

from vision_models import VisualAnalysisSummary


def summarize_visual_analysis(analysis: VisualAnalysisSummary) -> VisualAnalysisSummary:
    api_key = os.environ.get("MISTRAL_API_KEY", "")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY environment variable is required")

    client = Mistral(api_key=api_key)

    parts = []
    if analysis.description:
        parts.append(f"Description: {analysis.description}")
    if analysis.labels:
        parts.append(f"Labels: {', '.join(analysis.labels)}")
    if analysis.detected_text:
        parts.append(f"Detected text: {analysis.detected_text}")
    if not analysis.safety_is_safe:
        parts.append("Safety: flagged as potentially unsafe")

    prompt = (
        f"Summarize the following visual analysis of an image in 2-3 concise sentences:\n"
        f"{' '.join(parts)}"
    )

    chat_response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {
                "role": "system",
                "content": "You summarize visual analysis results concisely.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=256,
    )

    summary_text = chat_response.choices[0].message.content.strip()
    analysis.summary = summary_text
    return analysis
