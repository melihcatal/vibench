import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


class LiveCaptionSafetyChecker:
    def __init__(self):
        self.url = f"{PERSPECTIVE_API_URL}?key={PERSPECTIVE_API_KEY}"

    async def check_text_safety(self, text: str) -> dict:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
            "languages": ["en"],
        }
        response = requests.post(self.url, json=payload)
        response.raise_for_status()
        return response.json()


async def check_live_caption_safety(caption_stream):
    safety_checker = LiveCaptionSafetyChecker()
    async for caption in caption_stream:
        text = caption.get("text", "")
        safety_result = await safety_checker.check_text_safety(text)
        toxicity_score = (
            safety_result.get("attributeScores", {})
            .get("TOXICITY", {})
            .get("summaryScore", {})
            .get("value", 0)
        )
        yield {
            "text": text,
            "type": caption.get("type", "interim"),
            "toxicity_score": toxicity_score,
            "is_unsafe": toxicity_score > 0.7,
        }
