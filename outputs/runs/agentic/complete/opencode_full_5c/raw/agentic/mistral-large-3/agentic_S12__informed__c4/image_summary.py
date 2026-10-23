from openai import OpenAI
from typing import Dict, List
import json


def summarize_visual_analysis(
    labels: List[Dict], description: str, texts: List[Dict]
) -> str:
    """Summarizes visual analysis results using OpenAI's GPT model."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = (
        f"Summarize the following visual analysis results for an image:\n"
        f"Labels: {json.dumps(labels)}\n"
        f"Description: {description}\n"
        f"Detected Texts: {json.dumps(texts)}\n"
        "Provide a concise summary in 2-3 sentences."
    )

    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
