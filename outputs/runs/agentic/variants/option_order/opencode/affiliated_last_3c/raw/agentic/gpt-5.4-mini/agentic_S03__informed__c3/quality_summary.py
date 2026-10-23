from typing import Dict, List

from openai import OpenAI


MODEL_ID = "gpt-5.4-mini"


def quality_summary(issues: List[str]) -> Dict[str, str]:
    client = OpenAI()
    prompt = "Summarize translation quality issues: " + " | ".join(issues)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
    )
    return {
        "summary": response.choices[0].message.content or "",
        "provider": "openai",
        "model": MODEL_ID,
    }
