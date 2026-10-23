import os
from typing import Dict, Any, List
from datetime import datetime
from anthropic import Anthropic


class ClaimsModerator:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20240620"

    def moderate_claims(
        self, claims: Dict[str, Any], text_fields: List[str]
    ) -> Dict[str, Any]:
        moderated_results = {}
        for field in text_fields:
            if field in claims:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=100,
                    messages=[
                        {
                            "role": "user",
                            "content": f"Moderate the following text for inappropriate content: {claims[field]}",
                        }
                    ],
                )
                moderated_results[field] = {
                    "original": claims[field],
                    "moderated": response.content[0].text.strip(),
                    "flagged": "inappropriate" in response.content[0].text.lower(),
                }
        return moderated_results


if __name__ == "__main__":
    moderator = ClaimsModerator()
    sample_claims = {"name": "John Doe", "bio": "I hate everyone and everything."}
    result = moderator.moderate_claims(sample_claims, ["bio"])
    print("Moderation Results:", result)
