import os
from typing import List
from openai import OpenAI

from safety_client import get_openai_client
from safety_models import ModerationDecision, ModerationSummary

def summarize_moderation_decisions(decisions: List[ModerationDecision]) -> ModerationSummary:
    client = get_openai_client()
    
    decision_strings = []
    original_texts = []
    for i, decision in enumerate(decisions):
        original_texts.append(decision.original_text)
        decision_strings.append(
            f"Item {i+1}: Original Text: '{decision.original_text[:50]}...'
            Decision: {decision.decision}. Reasons: {', '.join(decision.reasons) if decision.reasons else 'None'}."
        )
    
    prompt = (
        "Summarize the following moderation decisions. Highlight the overall sentiment, "
        "any recurring issues, and the proportion of content that was flagged. "
        "Keep the summary concise and actionable for a reviewer."
        "\n\nModeration Decisions:\n" + "\n".join(decision_strings)
    )

    # Using a modern OpenAI model for summarization
    chat_completion = client.chat.completions.create(
        model="gpt-4o", # Concrete model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes content moderation decisions."},
            {"role": "user", "content": prompt}
        ]
    )

    summary_text = chat_completion.choices[0].message.content

    return ModerationSummary(
        original_texts=original_texts,
        decisions=decisions,
        summary_text=summary_text
    )
