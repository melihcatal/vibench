import os
import openai
from typing import List, Dict


def summarize_moderation_decisions(decisions: List[Dict[str, float]]) -> str:
    """
    Summarizes a list of moderation decisions using OpenAI's GPT-3.5 Turbo.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = "The following is a list of moderation scores for a batch of text. Please provide a brief summary of the overall safety of the content.\n\n"
    for i, decision in enumerate(decisions):
        prompt += f"Item {i + 1}:\n"
        for category, score in decision.items():
            prompt += f"- {category}: {score:.2f}\n"
        prompt += "\n"

    prompt += "Summary:"

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes content moderation results.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
