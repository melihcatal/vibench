import os
import anthropic
from vision_models import VisionAnalysis

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def image_summary(analysis: VisionAnalysis) -> str:
    labels_str = ", ".join(analysis["labels"]["labels"])
    desc = analysis["description"]["caption"]
    texts_str = ", ".join(analysis["detected_text"]["texts"])
    safety_str = str(analysis["safety"])
    prompt = f"""Provide a concise 1-2 sentence summary of the image based on this analysis:
Labels: {labels_str}
Description: {desc}
Detected text: {texts_str}
Safety ratings: {safety_str}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=150,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()
