import os
import requests

class ContentSafetyChecker:
    def __init__(self):
        self.api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
        self.endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
        if not self.api_key or not self.endpoint:
            raise ValueError("Azure Content Safety credentials not set")

    def check_text(self, text: str) -> dict:
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {"text": text}
        
        response = requests.post(
            f"{self.endpoint}/contentsafety/text:analyze",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

async def check_live_captions_safety(caption_stream):
    checker = ContentSafetyChecker()
    async for caption in caption_stream:
        result = checker.check_text(caption)
        is_unsafe = any(
            category["severity"] > 2 
            for category in result.get("categoriesAnalysis", [])
        )
        print(f"Caption: {caption} | Unsafe: {is_unsafe}")
        yield {"text": caption, "is_unsafe": is_unsafe}