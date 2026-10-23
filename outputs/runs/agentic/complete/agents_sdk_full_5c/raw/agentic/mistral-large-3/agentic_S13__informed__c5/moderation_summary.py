# Summarize moderation decisions using OpenAI GPT-4

import os
from typing import List, Dict
from openai import OpenAI
from safety_models import SafetyDecision


def summarize_moderation_decisions(decisions: List[Dict[str, List[SafetyDecision]]]) -> str:
    """Summarize moderation decisions using OpenAI GPT-4."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    decision_texts = []
    for decision_group in decisions:
        for text, decision_list in decision_group.items():
            flagged = [d["category"] for d in decision_list if d["flagged"]]
            if flagged:
                decision_texts.append(f"Text: '{text}' was flagged for: {', '.join(flagged)}.")
            else:
                decision_texts.append(f"Text: '{text}' was allowed.")
    
    prompt = (
        "Summarize the following moderation decisions in a concise report:\n\n"
        f"{'\n'.join(decision_texts)}"
    )
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
    )
    return response.choices[0].message.content.strip()