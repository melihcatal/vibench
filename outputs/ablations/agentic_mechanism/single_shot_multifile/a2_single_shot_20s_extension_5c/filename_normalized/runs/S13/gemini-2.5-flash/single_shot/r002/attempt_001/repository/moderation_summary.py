import os
from typing import List
from safety_client import get_openai_client
from safety_models import ModerationResult

def summarize_moderation_decisions(results: List[ModerationResult]) -> str:
    client = get_openai_client()
    
    summary_parts = []
    for i, res in enumerate(results):
        violations = [cat.category for cat in res.categories if cat.violates]
        status = res.overall_decision
        
        part = f"Item {i+1}: Status={status}. Violations: {', '.join(violations) if violations else 'None'}."
        part += f" Original text: '{res.text}'."
        if res.redacted_text and res.redacted_text != res.text:
            part += f" Redacted text: '{res.redacted_text}'."
        summary_parts.append(part)

    full_context = "\n".join(summary_parts)
    
    prompt = f"""Summarize the following moderation decisions. Highlight any unsafe content and the reasons.
    
    Moderation Results:
    {full_context}
    
    Provide a concise summary of all moderation outcomes, noting any potential actions needed."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes moderation reports."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content
