import os
from typing import Union
from openai import OpenAI
from security_models import SafetyCheckResult


class PayloadSafetyChecker:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def check_payload_safety(self, text: Union[str, bytes]) -> SafetyCheckResult:
        if isinstance(text, bytes):
            text = text.decode("utf-8")

        try:
            response = self.client.moderations.create(input=text)
            result = response.results[0]

            violations = {}
            if result.flagged:
                categories = result.categories.model_dump()
                violations = {k: v for k, v in categories.items() if v}

            return SafetyCheckResult(
                is_safe=not result.flagged,
                violations=violations,
                confidence=1.0 - max(result.category_scores.model_dump().values()),
            )
        except Exception as e:
            raise Exception(f"Payload safety check failed: {e}")
