import os
from anthropic import Anthropic
from vision_models import FullVisionAnalysis


def image_summary(analysis: FullVisionAnalysis) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""Summarize the following image analysis results in 1-2 sentences:

Labels: {", ".join(analysis.labels.labels)}
Description: {analysis.description.description}
Detected text: {", ".join(analysis.ocr.texts[:5])}
Safety scores: {analysis.safety.scores}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=100,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()
