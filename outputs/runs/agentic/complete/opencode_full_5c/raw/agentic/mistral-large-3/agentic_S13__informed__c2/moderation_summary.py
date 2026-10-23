from typing import List, Dict, Union
import os
from openai import OpenAI


def moderation_summary(
    moderation_results: List[Dict[str, Union[bool, Dict[str, int]]]],
    texts: List[str],
) -> str:
    """
    Summarize moderation decisions using OpenAI GPT-4.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key not configured")

    client = OpenAI(api_key=api_key)

    summary_prompt = (
        "Summarize the following moderation results in a concise report. "
        "Include the total number of flagged messages, common reasons, and any patterns.\n\n"
        "Moderation Results:\n"
    )

    for i, result in enumerate(moderation_results):
        decision = result.get("decision", False)
        scores = result.get("scores", {})
        text_preview = texts[i][:50] + "..." if len(texts[i]) > 50 else texts[i]
        summary_prompt += (
            f"Message {i + 1}: {text_preview}\n"
            f"Decision: {'Flagged' if decision else 'Allowed'}\n"
            f"Scores: {scores}\n\n"
        )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a moderation assistant."},
            {"role": "user", "content": summary_prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()
