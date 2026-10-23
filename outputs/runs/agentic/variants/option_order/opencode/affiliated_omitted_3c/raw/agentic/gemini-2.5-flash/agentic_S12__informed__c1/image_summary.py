import os
from anthropic import Anthropic


def summarize_visual_analysis(
    image_description: str, image_labels: list[str], detected_text: str
) -> str:
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""You are an AI assistant tasked with summarizing visual analysis results.
Image Description: {image_description}
Image Labels: {", ".join(image_labels)}
Detected Text: {detected_text}

Please provide a concise summary of the visual content based on the information above."""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
