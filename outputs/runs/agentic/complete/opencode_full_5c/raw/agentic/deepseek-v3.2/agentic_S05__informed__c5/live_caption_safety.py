import os
import requests
from typing import Dict, List, Optional, Tuple


class LiveCaptionSafetyChecker:
    """Check live transcript text for unsafe content using Perspective API."""

    def __init__(self):
        self.api_key = os.getenv("PERSPECTIVE_API_KEY")
        if not self.api_key:
            raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

        self.api_url = (
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        )

        # Define attributes to check
        self.toxicity_attributes = {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        }

    def check_text_safety(self, text: str, languages: List[str] = None) -> Dict:
        """Check text for unsafe content using Perspective API."""
        if not text or not text.strip():
            return {"safe": True, "scores": {}, "message": "Empty text"}

        payload = {
            "comment": {"text": text},
            "languages": languages or ["en"],
            "requestedAttributes": self.toxicity_attributes,
            "doNotStore": True,
        }

        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}", json=payload, timeout=5
            )
            response.raise_for_status()

            result = response.json()
            return self._parse_safety_result(result)

        except requests.exceptions.RequestException as e:
            print(f"Perspective API error: {e}")
            return {
                "safe": True,
                "scores": {},
                "error": str(e),
                "message": "API error, assuming safe",
            }

    def _parse_safety_result(self, api_result: Dict) -> Dict:
        """Parse Perspective API result into safety scores."""
        attribute_scores = api_result.get("attributeScores", {})

        scores = {}
        for attr_name, attr_data in attribute_scores.items():
            summary_score = attr_data.get("summaryScore", {})
            scores[attr_name] = {
                "value": summary_score.get("value", 0),
                "type": summary_score.get("type", "UNKNOWN"),
            }

        # Determine if text is safe based on thresholds
        is_safe = self._determine_safety(scores)

        return {
            "safe": is_safe,
            "scores": scores,
            "flagged_attributes": self._get_flagged_attributes(scores),
        }

    def _determine_safety(self, scores: Dict) -> bool:
        """Determine if text is safe based on score thresholds."""
        thresholds = {
            "TOXICITY": 0.7,
            "SEVERE_TOXICITY": 0.8,
            "IDENTITY_ATTACK": 0.7,
            "INSULT": 0.7,
            "PROFANITY": 0.8,
            "THREAT": 0.8,
            "SEXUALLY_EXPLICIT": 0.8,
            "FLIRTATION": 0.9,
        }

        for attr_name, threshold in thresholds.items():
            if attr_name in scores:
                score_value = scores[attr_name]["value"]
                if score_value >= threshold:
                    return False

        return True

    def _get_flagged_attributes(self, scores: Dict) -> List[str]:
        """Get list of attributes that exceed thresholds."""
        thresholds = {
            "TOXICITY": 0.7,
            "SEVERE_TOXICITY": 0.8,
            "IDENTITY_ATTACK": 0.7,
            "INSULT": 0.7,
            "PROFANITY": 0.8,
            "THREAT": 0.8,
            "SEXUALLY_EXPLICIT": 0.8,
            "FLIRTATION": 0.9,
        }

        flagged = []
        for attr_name, threshold in thresholds.items():
            if attr_name in scores:
                score_value = scores[attr_name]["value"]
                if score_value >= threshold:
                    flagged.append(f"{attr_name}: {score_value:.3f}")

        return flagged

    async def check_caption_stream(self, caption_stream, languages: List[str] = None):
        """Check a stream of captions for safety."""
        async for caption in caption_stream:
            if caption and caption.strip():
                safety_result = self.check_text_safety(caption, languages)

                if not safety_result["safe"]:
                    print(f"⚠️  UNSAFE CAPTION DETECTED: {caption}")
                    print(
                        f"   Flagged attributes: {safety_result['flagged_attributes']}"
                    )

                yield {
                    "text": caption,
                    "safe": safety_result["safe"],
                    "scores": safety_result["scores"],
                    "flagged": safety_result["flagged_attributes"],
                }
            else:
                yield {"text": caption, "safe": True, "scores": {}, "flagged": []}

    def get_safety_summary(self, safety_results: List[Dict]) -> Dict:
        """Generate safety summary from multiple results."""
        total = len(safety_results)
        unsafe_count = sum(1 for r in safety_results if not r["safe"])

        # Calculate average scores for each attribute
        avg_scores = {}
        if safety_results:
            all_scores = [r["scores"] for r in safety_results if r["scores"]]
            if all_scores:
                for attr_name in self.toxicity_attributes.keys():
                    attr_scores = [
                        s.get(attr_name, {}).get("value", 0)
                        for s in all_scores
                        if attr_name in s
                    ]
                    if attr_scores:
                        avg_scores[attr_name] = sum(attr_scores) / len(attr_scores)

        return {
            "total_captions": total,
            "unsafe_captions": unsafe_count,
            "safety_percentage": ((total - unsafe_count) / total * 100)
            if total > 0
            else 100,
            "average_scores": avg_scores,
            "recommendation": "Continue monitoring"
            if unsafe_count == 0
            else "Review flagged content",
        }


async def mock_unsafe_caption_stream():
    """Mock caption stream with some unsafe content for testing."""
    captions = [
        "Hello everyone, welcome to the meeting.",
        "This is a normal business discussion.",
        "You're all idiots who don't understand anything!",  # Unsafe
        "Let's focus on the quarterly results.",
        "I'm going to hurt anyone who disagrees with me!",  # Unsafe
        "Thank you for your attention.",
    ]

    for caption in captions:
        yield caption
        await asyncio.sleep(0.3)


async def test_safety_checking():
    """Test live caption safety checking."""
    print("Testing live caption safety with Perspective API...")

    checker = LiveCaptionSafetyChecker()

    # Test individual texts
    test_texts = [
        "Hello, how are you today?",
        "You're a complete moron!",  # Should be flagged
        "The weather is nice outside.",
        "I hate you and everyone like you!",  # Should be flagged
        "Let's schedule the next meeting.",
    ]

    print("\nTesting individual texts:")
    for text in test_texts:
        result = checker.check_text_safety(text)
        status = "✅ SAFE" if result["safe"] else "❌ UNSAFE"
        print(f"{status}: {text}")
        if result["flagged_attributes"]:
            print(f"  Flagged: {result['flagged_attributes']}")

    # Test streaming
    print("\n\nTesting streaming safety check:")
    safety_results = []

    async for result in checker.check_caption_stream(mock_unsafe_caption_stream()):
        status = "✅" if result["safe"] else "❌"
        print(f"{status} {result['text']}")
        safety_results.append(result)

    # Generate summary
    print("\nSafety Summary:")
    summary = checker.get_safety_summary(safety_results)
    for key, value in summary.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    asyncio.run(test_safety_checking())
