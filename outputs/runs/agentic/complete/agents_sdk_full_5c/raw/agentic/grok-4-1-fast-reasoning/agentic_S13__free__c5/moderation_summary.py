from openai import OpenAI
from typing import List
from safety_client import get_openai_api_key
from safety_models import SafetyDecision

def moderation_summary(decisions: List[SafetyDecision]) -> str:
    client = OpenAI(api_key=get_openai_api_key())
    context = "\n".join(
        [f"Item {i+1}: flagged={d.flagged}, categories={dict(d.categories)}" for i, d in enumerate(decisions)]
    )
    messages = [
        {"role": "system", "content": "Summarize moderation decisions concisely, highlighting patterns and issues."},
        {"role": "user", "content": f"Summarize:\n{context}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=500
    )
    return response.choices[0].message.content
