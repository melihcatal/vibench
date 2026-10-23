# Summarize Moderation Decisions
from typing import List
from openai import OpenAI
from safety_models import TextModerationResult


class ModerationSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key="your-openai-api-key")

    def summarize_decisions(self, results: List[TextModerationResult]) -> str:
        """Summarize moderation decisions using OpenAI GPT-4."""
        prompt = (
            "Summarize the following moderation decisions in a concise report:\n"
            f"{results}\n"
            "Focus on blocked content and flagged categories."
        )
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()