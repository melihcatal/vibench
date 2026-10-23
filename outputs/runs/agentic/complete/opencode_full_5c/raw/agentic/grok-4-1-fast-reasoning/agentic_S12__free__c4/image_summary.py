import os
from openai import OpenAI
from vision_client import OPENAI_API_KEY


def image_summary(analysis: dict) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"""Summarize these image analysis results concisely:

Labels: {analysis.get("labels", [])}
Description: {analysis.get("description", "")}
Text: {analysis.get("texts", [])}
Safety: {analysis.get("safety", {})}

Provide a one-paragraph summary."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
    )
    return response.choices[0].message.content
