import os
from typing import List
from openai import OpenAI

def quality_summary(source_texts: List[str], translated_texts: List[str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    client = OpenAI(api_key=api_key)
    
    pairs_str = "\n".join(f"{s} → {t}" for s, t in zip(source_texts, translated_texts))
    prompt = f"""You are a professional translation quality assessor. Analyze the following source-target translation pairs and provide a concise summary of any quality issues (inaccuracies, unnatural phrasing, omissions, cultural issues). If excellent, state so.

Translation pairs:
{pairs_str}"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Be concise. Use bullet points for issues or state 'No issues detected.'"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.1
    )
    return response.choices[0].message.content.strip()
