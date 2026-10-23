import os
from openai import OpenAI

def quality_summary(original: str, translated: str, source_lang: str, target_lang: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Summarize translation quality issues from {source_lang} to {target_lang}.

Original: {original}

Translated: {translated}

Focus on accuracy, fluency, omissions, awkward phrasing, or cultural issues. If excellent, state that."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a translation quality expert."},
                  {"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()
