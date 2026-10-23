import os
from openai import OpenAI
import vision_models


def image_summary(analysis: vision_models.VisualAnalysis) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Provide a concise summary of this image analysis:
- Labels: {", ".join(analysis["labels"])}
- Description: {analysis["description"]}
- Detected text: {", ".join(analysis["texts"])}
- Safety likelihoods: {analysis["safety"]}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100,
    )
    return response.choices[0].message.content.strip()
