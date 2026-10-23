from google.cloud import language_v1
from typing import List, Dict, Any, Optional
import asyncio


class CaptionSafetyChecker:
    def __init__(self, project_id: Optional[str] = None):
        self.client = language_v1.LanguageServiceClient()
        self.project_id = project_id

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        response = self.client.analyze_sentiment(request={"document": document})

        return {
            "score": response.document_sentiment.score,
            "magnitude": response.document_sentiment.magnitude,
            "sentences": [
                {
                    "text": sentence.text.content,
                    "score": sentence.sentiment.score,
                    "magnitude": sentence.sentiment.magnitude,
                }
                for sentence in response.sentences
            ],
        }

    def analyze_entities(self, text: str) -> Dict[str, Any]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        response = self.client.analyze_entities(request={"document": document})

        entities = []
        for entity in response.entities:
            entities.append(
                {
                    "name": entity.name,
                    "type": language_v1.Entity.Type(entity.type_).name,
                    "salience": entity.salience,
                    "metadata": dict(entity.metadata),
                }
            )

        return {"entities": entities, "language": response.language}

    def analyze_entity_sentiment(self, text: str) -> Dict[str, Any]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        response = self.client.analyze_entity_sentiment(request={"document": document})

        entity_sentiments = []
        for entity in response.entities:
            entity_sentiments.append(
                {
                    "name": entity.name,
                    "type": language_v1.Entity.Type(entity.type_).name,
                    "salience": entity.salience,
                    "sentiment_score": entity.sentiment.score,
                    "sentiment_magnitude": entity.sentiment.magnitude,
                }
            )

        return {"entity_sentiments": entity_sentiments, "language": response.language}

    def classify_text(self, text: str) -> Dict[str, Any]:
        document = language_v1.Document(
            content=text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
        )

        response = self.client.classify_text(request={"document": document})

        categories = []
        for category in response.categories:
            categories.append(
                {"name": category.name, "confidence": category.confidence}
            )

        return {"categories": categories}

    def check_safety(self, caption: str) -> Dict[str, Any]:
        sentiment = self.analyze_sentiment(caption)
        entities = self.analyze_entities(caption)

        is_safe = True
        safety_issues = []

        if sentiment["score"] < -0.5:
            is_safe = False
            safety_issues.append("Highly negative sentiment")

        if sentiment["magnitude"] > 2.0:
            safety_issues.append("Strong emotional content")

        for entity in entities["entities"]:
            if entity["type"] in ["PERSON", "LOCATION", "ORGANIZATION"]:
                safety_issues.append(
                    f"Contains {entity['type'].lower()}: {entity['name']}"
                )

        return {
            "is_safe": is_safe,
            "safety_issues": safety_issues,
            "sentiment": sentiment,
            "entities": entities,
            "caption": caption,
        }

    async def check_stream_safety(self, caption_stream):
        async for caption, is_final in caption_stream:
            safety_result = self.check_safety(caption)
            yield {**safety_result, "is_final": is_final}

    def get_toxicity_score(self, text: str) -> float:
        sentiment = self.analyze_sentiment(text)
        return max(0.0, -sentiment["score"])

    def flag_inappropriate_content(self, text: str, threshold: float = 0.7) -> bool:
        toxicity = self.get_toxicity_score(text)
        return toxicity > threshold

    def create_safety_report(self, captions: List[str]) -> Dict[str, Any]:
        reports = []
        unsafe_count = 0

        for caption in captions:
            safety = self.check_safety(caption)
            reports.append(safety)
            if not safety["is_safe"]:
                unsafe_count += 1

        return {
            "total_captions": len(captions),
            "unsafe_captions": unsafe_count,
            "safety_percentage": ((len(captions) - unsafe_count) / len(captions)) * 100
            if captions
            else 100,
            "reports": reports,
        }
