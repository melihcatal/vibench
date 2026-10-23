import os
from openai import OpenAI
from vision_client import get_openai_client
from vision_models import SummaryInput

def summarize_visual_analysis(summary_input: SummaryInput) -> str:
    client = get_openai_client()

    labels_str = ", ".join(summary_input.labels)
    text_snippets_str = ", ".join(summary_input.detected_text_snippets)
    safety_warnings_str = ", ".join(summary_input.safety_warnings) if summary_input.safety_warnings else "None."

    prompt = f"""
    Based on the following visual analysis results, generate a concise summary.

    Image Description: {summary_input.description}
    Detected Labels/Objects: {labels_str if labels_str else 'None.'}
    Detected Text: {text_snippets_str if text_snippets_str else 'None.'}
    Safety Warnings: {safety_warnings_str}

    Summarize the key visual elements and any notable safety concerns in a short paragraph (max 3 sentences).
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes visual analysis results."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return response.choices[0].message.content.strip()