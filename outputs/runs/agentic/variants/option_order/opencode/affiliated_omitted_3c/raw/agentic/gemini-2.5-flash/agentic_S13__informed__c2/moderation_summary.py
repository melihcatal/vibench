import os
from typing import List
from openai import OpenAI
from safety_models import TextModerationResponse


def summarize_moderation_decisions(
    moderation_results: List[TextModerationResponse],
) -> str:
    """
    Summarizes a list of moderation decisions using OpenAI's chat completions API.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Prepare the input for the LLM
    summary_input = ""
    for i, res in enumerate(moderation_results):
        summary_input += f"Message {i + 1}: '{res.text}' - Decisions: "
        if res.results:
            summary_input += ", ".join(
                [f"{r.category} (Severity: {r.severity})" for r in res.results]
            )
        else:
            summary_input += "No issues detected."
        summary_input += "\n"

    prompt = f"""Summarize the following text moderation results. Highlight any severe issues and overall trends.\n\n{summary_input}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a common chat model for summarization
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes moderation decisions.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content
