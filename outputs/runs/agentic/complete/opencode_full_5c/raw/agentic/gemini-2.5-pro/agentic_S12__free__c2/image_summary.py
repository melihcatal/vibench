import os
import openai
from typing import List, Dict, Any


def summarize_visual_analysis(analysis_results: Dict[str, Any]) -> str:
    """Summarizes visual analysis results using OpenAI's GPT-3.5 Turbo."""

    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"Summarize the following visual analysis results into a concise paragraph:\n\n{analysis_results}"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes visual analysis data.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
