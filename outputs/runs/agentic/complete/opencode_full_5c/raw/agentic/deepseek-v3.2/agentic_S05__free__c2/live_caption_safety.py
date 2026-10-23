from google.cloud import language_v1
from typing import Dict, Any, List, Generator
import time


class CaptionSafetyChecker:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        try:
            response = self.client.analyze_sentiment(request={"document": document})

            return {
                "sentiment_score": response.document_sentiment.score,
                "sentiment_magnitude": response.document_sentiment.magnitude,
                "language": response.language,
                "sentences": [
                    {
                        "text": sentence.text.content,
                        "sentiment_score": sentence.sentiment.score,
                        "sentiment_magnitude": sentence.sentiment.magnitude,
                    }
                    for sentence in response.sentences
                ],
            }
        except Exception as e:
            return {
                "error": str(e),
                "sentiment_score": 0.0,
                "sentiment_magnitude": 0.0,
            }

    def analyze_entities(self, text: str) -> Dict[str, Any]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        try:
            response = self.client.analyze_entities(request={"document": document})

            entities = []
            for entity in response.entities:
                entity_info = {
                    "name": entity.name,
                    "type": language_v1.Entity.Type(entity.type_).name,
                    "salience": entity.salience,
                    "metadata": dict(entity.metadata),
                }

                if entity.sentiment:
                    entity_info["sentiment_score"] = entity.sentiment.score
                    entity_info["sentiment_magnitude"] = entity.sentiment.magnitude

                entities.append(entity_info)

            return {
                "entities": entities,
                "language": response.language,
            }
        except Exception as e:
            return {
                "error": str(e),
                "entities": [],
            }

    def classify_text(self, text: str) -> Dict[str, Any]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        try:
            response = self.client.classify_text(request={"document": document})

            categories = []
            for category in response.categories:
                categories.append(
                    {
                        "name": category.name,
                        "confidence": category.confidence,
                    }
                )

            return {
                "categories": categories,
                "language": response.language,
            }
        except Exception as e:
            return {
                "error": str(e),
                "categories": [],
            }

    def check_safety(self, text: str) -> Dict[str, Any]:
        safety_analysis = {
            "text": text,
            "timestamp": time.time(),
            "sentiment_analysis": self.analyze_sentiment(text),
            "entity_analysis": self.analyze_entities(text),
            "content_classification": self.classify_text(text),
            "safety_flags": [],
        }

        sentiment = safety_analysis["sentiment_analysis"]
        if sentiment.get("sentiment_score", 0) < -0.5:
            safety_analysis["safety_flags"].append("NEGATIVE_SENTIMENT")

        if sentiment.get("sentiment_magnitude", 0) > 2.0:
            safety_analysis["safety_flags"].append("HIGH_EMOTIONAL_INTENSITY")

        entities = safety_analysis["entity_analysis"].get("entities", [])
        for entity in entities:
            if entity.get("type") in ["PERSON", "LOCATION", "ORGANIZATION"]:
                safety_analysis["safety_flags"].append(f"CONTAINS_{entity['type']}")

        categories = safety_analysis["content_classification"].get("categories", [])
        for category in categories:
            if "/Law & Government" in category.get("name", ""):
                safety_analysis["safety_flags"].append("LAW_GOVERNMENT_CONTENT")
            if "/News" in category.get("name", ""):
                safety_analysis["safety_flags"].append("NEWS_CONTENT")

        safety_analysis["is_safe"] = len(safety_analysis["safety_flags"]) == 0

        return safety_analysis

    def monitor_caption_safety(
        self, caption_stream: Generator[Dict[str, Any], None, None]
    ) -> Generator[Dict[str, Any], None, None]:
        for caption in caption_stream:
            if caption.get("is_final", False):
                transcript = caption.get("transcript", "")

                if transcript.strip():
                    safety_check = self.check_safety(transcript)

                    yield {
                        **caption,
                        "safety_analysis": safety_check,
                        "is_safe": safety_check["is_safe"],
                        "safety_flags": safety_check["safety_flags"],
                    }
                else:
                    yield {**caption, "is_safe": True, "safety_flags": []}
            else:
                yield {**caption, "is_safe": True, "safety_flags": []}


def check_live_caption_safety(caption_stream):
    checker = CaptionSafetyChecker()

    for safety_result in checker.monitor_caption_safety(caption_stream):
        if "safety_analysis" in safety_result:
            analysis = safety_result["safety_analysis"]
            flags = safety_result["safety_flags"]

            if flags:
                print(f"SAFETY ALERT: {flags}")
                print(f"Text: {analysis['text']}")
                print(
                    f"Sentiment: {analysis['sentiment_analysis'].get('sentiment_score', 0):.2f}"
                )
                print("-" * 50)

        yield safety_result


if __name__ == "__main__":
    test_captions = [
        {
            "transcript": "This is a normal meeting about project updates",
            "is_final": True,
        },
        {"transcript": "I'm very angry about the decision", "is_final": True},
        {"transcript": "Partial result", "is_final": False},
    ]

    for result in check_live_caption_safety(test_captions):
        print(result)
