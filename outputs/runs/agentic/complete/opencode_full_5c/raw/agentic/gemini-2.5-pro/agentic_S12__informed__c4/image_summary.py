import os
import openai
from vision_models import VisualAnalysis

openai.api_key = os.getenv("OPENAI_API_KEY")


def summarize_analysis(analysis: VisualAnalysis) -> str:
    prompt_parts = ["Summarize the following visual analysis results:\n"]

    if analysis.description:
        prompt_parts.append(f"- Description: {analysis.description.text}")

    if analysis.labels:
        labels_str = ", ".join([label.name for label in analysis.labels])
        prompt_parts.append(f"- Labels: {labels_str}")

    if analysis.text:
        text_str = ", ".join([t.text for t in analysis.text])
        prompt_parts.append(f"- Detected Text: {text_str}")

    if analysis.safety_scores:
        safety_str = ", ".join(
            [f"{s.category} ({s.probability:.2f})" for s in analysis.safety_scores]
        )
        prompt_parts.append(f"- Safety Assessment: {safety_str}")

    prompt = "\n".join(prompt_parts)

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a visual analysis summarizer."},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content
