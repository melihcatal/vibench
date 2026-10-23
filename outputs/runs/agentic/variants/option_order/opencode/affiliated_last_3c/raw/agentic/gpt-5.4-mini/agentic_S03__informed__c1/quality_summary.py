import os
from typing import Dict, List

import openai


class QualitySummaryClient:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("OPENAI_QUALITY_MODEL", "gpt-5.4-mini")

    def summarize(self, issues: List[str]) -> Dict[str, str]:
        prompt = "Summarize translation quality issues concisely: " + " | ".join(issues)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"summary": response.choices[0].message.content or "", "model": self.model}


def quality_summary(issues: List[str]) -> Dict[str, str]:
    return QualitySummaryClient().summarize(issues)
