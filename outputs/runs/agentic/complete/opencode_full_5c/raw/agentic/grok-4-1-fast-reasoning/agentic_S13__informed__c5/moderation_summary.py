import os
from typing import List
from openai import OpenAI
from safety_models import SafetyResult

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderation_summary(results: List[SafetyResult]) -> str:
    items = []
    for r in results:
        preview = (
            (r["input_text"][:100] + "...")
            if len(r["input_text"]) > 100
            else r["input_text"]
        )
        flags = ", ".join(r["flagged_categories"]) or "none"
        items.append(
            f"- Preview: {preview}\\n  Blocked: {r['blocked']}, Flags: {flags}"
        )

    context = "\\n".join(items)
    prompt = f"""Summarize these moderation results in 2-3 sentences, including stats like num blocked/total, common categories:

{context}"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=400,
    )
    return resp.choices[0].message.content
