import os
import requests

# Example: using Perspective API for unsafe content detection
# Provider: Perspective API (service=Perspective API)
# Configuration:
#   PERSPECTIVE_API_KEY must be set in the environment.


class LiveCaptionSafety:
    """
    Detects unsafe content in live transcript chunks using Perspective API.
    Yields a flag indicating whether the chunk is safe or contains toxic content.
    """

    def __init__(self, attribute_scores: list = ["TOXICITY"]):
        self.attribute_scores = attribute_scores
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")
        self.headers = {
            "x-api-key": self.api_key,
            "content-type": "application/json",
        }
        self.endpoint = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

    def is_safe(self, text: str) -> bool:
        """Check a single text chunk."""
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {attr: {} for attr in self.attribute_scores},
        }
        resp = requests.post(self.endpoint, json=payload, headers=self.headers)
        resp.raise_for_status()
        scores = resp.json()["attributeScores"]
        for attr in self.attribute_scores:
            score = scores[attr]["summaryScore"]["value"]
            # Threshold can be tuned; here we consider >0.5 as unsafe
            if score > 0.5:
                return False
        return True

    async def safe_stream(self, transcript_stream):
        """Streaming wrapper yielding only safe chunks."""
        for chunk in transcript_stream:
            if self.is_safe(chunk):
                yield {"text": chunk, "safe": True}
            else:
                yield {"text": chunk, "safe": False, "reason": "unsafe"}


if __name__ == "__main__":
    # Demo with dummy text generator
    async def dummy_stream():
        for i in range(4):
            yield f"This is a test comment {i}."

    safety_checker = LiveCaptionSafety()
    asyncio.run(safety_checker.safe_stream(dummy_stream()))
