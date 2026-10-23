import os
from anthropic import Anthropic
from typing import Dict, Any


class OnboardingSummarizer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20240620"

    def summarize_onboarding(self, onboarding_data: Dict[str, Any]) -> str:
        prompt = (
            f"Summarize the following onboarding data for support review:\n"
            f"{onboarding_data}\n\n"
            f"Provide a concise summary highlighting key details and potential issues."
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text