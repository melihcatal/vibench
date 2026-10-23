from typing import List

import openai

from vision_client import get_openai_client
from vision_models import VisualAnalysis

def generate_summary(analysis: VisualAnalysis) -> str:
    """
    Summarizes the visual analysis results using OpenAI's GPT-4o.

    Args:
        analysis: A VisualAnalysis object containing labels, description, text, and safety info.

    Returns:
        A concise summary string.
    """
    client: openai.OpenAI = get_openai_client()

    prompt_lines = ["Summarize the following analysis of an image:"]

    if analysis.description:
        prompt_lines.append(f"- Visual Description: {analysis.description.text}")

    if analysis.labels:
        label_names = ", ".join([label.name for label in analysis.labels])
        prompt_lines.append(f"- Detected objects/labels: {label_names}")

    if analysis.text:
        detected_text = ' | '.join([txt.text for txt in analysis.text])
        prompt_lines.append(f"- Text found in image: \"{detected_text}\"")
        
    if analysis.safety:
        if analysis.safety.safe:
            prompt_lines.append("- Safety status: Image is considered safe.")
        else:
            safety_issues = ", ".join([label.name for label in analysis.safety.labels])
            prompt_lines.append(f"- Safety concerns detected: {safety_issues}")

    prompt = "\n".join(prompt_lines)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that creates concise summaries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=150,
    )
    
    return response.choices[0].message.content
