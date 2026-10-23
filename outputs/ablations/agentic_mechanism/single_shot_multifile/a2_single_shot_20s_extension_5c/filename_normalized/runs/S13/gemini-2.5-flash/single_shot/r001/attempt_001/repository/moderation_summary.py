import os
from openai import OpenAI
from typing import List

from safety_client import get_openai_client
from safety_models import SummarizationInput, SummarizationOutput

def summarize_moderation_decisions(summary_input: SummarizationInput) -> SummarizationOutput:
    client = get_openai_client()

    # Construct the prompt for summarization
    prompt = f"Summarize the moderation decision for the following text.\n\nText: {summary_input.decision_text}\nFlagged Categories: {', '.join(summary_input.flagged_categories) if summary_input.flagged_categories else 'None'}\n\nProvide a concise summary of why this content was flagged or allowed, mentioning relevant categories. Start directly with the summary, no preamble."

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes moderation decisions.",
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o", # Concrete model identifier
            temperature=0.3,
            max_tokens=150,
        )

        summary = chat_completion.choices[0].message.content.strip()
        return SummarizationOutput(summary=summary)
    except Exception as e:
        print(f"Error summarizing moderation decisions with OpenAI: {e}")
        return SummarizationOutput(summary="Could not generate summary due to an error.")
