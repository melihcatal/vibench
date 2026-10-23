import os
from typing import Optional
from openai import OpenAI
from safety_models import ModerationResult


class RedactionClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required.")
        self.client = OpenAI(api_key=self.api_key)

    def redact(self, text: str, moderation_result: ModerationResult) -> str:
        unsafe_categories = [k for k, v in moderation_result.categories.items() if v]
        if not unsafe_categories:
            return text

        prompt = (
            f"Redact the following text by replacing unsafe content with '[REDACTED]'. "
            f"Unsafe categories: {', '.join(unsafe_categories)}. "
            f"Text: {text}"
        )
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=1000,
            temperature=0.0
        )
        return response.choices[0].message.content.strip()


def redact_unsafe(text: str, moderation_result: ModerationResult) -> str:
    client = RedactionClient()
    return client.redact(text, moderation_result)