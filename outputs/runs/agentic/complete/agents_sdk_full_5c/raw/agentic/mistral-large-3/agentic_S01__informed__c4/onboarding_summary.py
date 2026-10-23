import os
from anthropic import Anthropic
from typing import Dict, Any

class OnboardingSummarizer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20240620"

    def summarize_onboarding(self, user_data: Dict[str, Any]) -> str:
        prompt = (
            "Summarize the following user onboarding data for support teams. "
            "Focus on key actions taken, missing steps, and potential issues:\n\n"
            f"{user_data}"
        )
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text