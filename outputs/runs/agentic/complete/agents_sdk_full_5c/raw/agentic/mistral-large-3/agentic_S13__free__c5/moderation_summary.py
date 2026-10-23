import os
from typing import List, Dict
from openai import OpenAI
from safety_models import ModerationResult


class SummaryClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required.")
        self.client = OpenAI(api_key=self.api_key)

    def summarize_moderation(self, results: List[ModerationResult]) -> str:
        summary_prompt = (
            "Summarize the following moderation results in a concise report. "
            "Include the number of flagged messages and the top categories:"
            f"{results}"
        )
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": summary_prompt}],
            max_tokens=500,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()


def generate_moderation_summary(results: List[ModerationResult]) -> str:
    client = SummaryClient()
    return client.summarize_moderation(results)