import os
import json
from typing import List, Dict
import openai


def summarize_moderation_decisions(decisions: List[Dict]) -> str:
    """
    Summarizes a list of moderation decisions using OpenAI's GPT model.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    prompt = f"""
    The following is a list of moderation decisions in JSON format.
    Provide a concise summary of these decisions, highlighting any trends
    or important patterns.

    Decisions:
    {json.dumps(decisions, indent=2)}

    Summary:
    """

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant for content moderation teams.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.5,
        max_tokens=250,
    )

    return response.choices[0].message.content
