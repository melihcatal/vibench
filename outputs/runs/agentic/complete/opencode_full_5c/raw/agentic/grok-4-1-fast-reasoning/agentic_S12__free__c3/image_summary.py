from anthropic import Anthropic
from vision_models import FullVisionAnalysis


def image_summary(analysis: FullVisionAnalysis) -> str:
    client = Anthropic()
    prompt = f"""Summarize these visual analysis results in one paragraph:

Description: {analysis.description.description}
Labels: {", ".join(analysis.labels.labels)}
Detected Text: {analysis.text.text[:200]}...
Safety Score: {analysis.safety.score:.2f} ({analysis.safety.categories})

Focus on key visual elements, content, and safety."""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()
