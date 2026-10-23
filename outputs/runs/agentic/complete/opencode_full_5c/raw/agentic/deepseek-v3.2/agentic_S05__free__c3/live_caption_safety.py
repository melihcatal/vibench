from google.cloud import language_v1
from typing import Generator, Dict, Any, List, Tuple
import asyncio


class LiveCaptionSafetyChecker:
    def __init__(self, threshold: float = 0.7):
        self.client = language_v1.LanguageServiceClient()
        self.threshold = threshold
        self.toxic_categories = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        if not text.strip():
            return {"score": 0.0, "magnitude": 0.0}

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        try:
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
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {"score": 0.0, "magnitude": 0.0, "error": str(e)}

    def analyze_entities(self, text: str) -> Dict[str, Any]:
        if not text.strip():
            return {"entities": []}

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        try:
            response = self.client.analyze_entities(request={"document": document})

            entities = []
            for entity in response.entities:
                entities.append(
                    {
                        "name": entity.name,
                        "type": language_v1.Entity.Type(entity.type_).name,
                        "salience": entity.salience,
                        "mentions": [
                            {
                                "text": mention.text.content,
                                "type": language_v1.EntityMention.Type(
                                    mention.type_
                                ).name,
                            }
                            for mention in entity.mentions
                        ],
                    }
                )

            return {"entities": entities}
        except Exception as e:
            print(f"Entity analysis error: {e}")
            return {"entities": [], "error": str(e)}

    def check_toxicity(self, text: str) -> Dict[str, Any]:
        if not text.strip():
            return {category: 0.0 for category in self.toxic_categories}

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        try:
            request = language_v1.AnalyzeSentimentRequest(
                document=document,
                features={
                    "extract_document_sentiment": True,
                    "extract_entity_sentiment": True,
                    "classify_text": False,
                },
            )

            response = self.client.analyze_sentiment(request=request)

            toxicity_scores = {}
            for category in self.toxic_categories:
                toxicity_scores[category] = 0.0

            if hasattr(response, "document_sentiment"):
                score = response.document_sentiment.score
                if score < -0.5:
                    toxicity_scores["TOXICITY"] = 0.8
                elif score < -0.2:
                    toxicity_scores["TOXICITY"] = 0.5

            return toxicity_scores
        except Exception as e:
            print(f"Toxicity check error: {e}")
            return {category: 0.0 for category in self.toxic_categories}

    def is_unsafe(self, text: str) -> Tuple[bool, Dict[str, Any]]:
        toxicity_scores = self.check_toxicity(text)

        max_toxicity = max(toxicity_scores.values())
        is_unsafe = max_toxicity > self.threshold

        analysis = {
            "toxicity_scores": toxicity_scores,
            "max_toxicity": max_toxicity,
            "sentiment": self.analyze_sentiment(text),
            "entities": self.analyze_entities(text),
            "threshold": self.threshold,
            "is_unsafe": is_unsafe,
        }

        return is_unsafe, analysis

    def filter_unsafe_captions(
        self, caption_stream: Generator[Dict[str, Any], None, None]
    ) -> Generator[Dict[str, Any], None, None]:
        for caption in caption_stream:
            transcript = caption.get("transcript", "")

            is_unsafe, analysis = self.is_unsafe(transcript)

            filtered_caption = caption.copy()
            filtered_caption["safety_analysis"] = analysis
            filtered_caption["is_unsafe"] = is_unsafe

            if not is_unsafe:
                yield filtered_caption

    async def filter_unsafe_captions_async(
        self, caption_stream
    ) -> Generator[Dict[str, Any], None, None]:
        async for caption in caption_stream:
            transcript = caption.get("transcript", "")

            is_unsafe, analysis = await asyncio.to_thread(self.is_unsafe, transcript)

            filtered_caption = caption.copy()
            filtered_caption["safety_analysis"] = analysis
            filtered_caption["is_unsafe"] = is_unsafe

            if not is_unsafe:
                yield filtered_caption


def create_safety_filter_pipeline(
    caption_stream: Generator[Dict[str, Any], None, None], threshold: float = 0.7
) -> Generator[Dict[str, Any], None, None]:

    safety_checker = LiveCaptionSafetyChecker(threshold=threshold)
    return safety_checker.filter_unsafe_captions(caption_stream)


async def create_async_safety_filter_pipeline(caption_stream, threshold: float = 0.7):

    safety_checker = LiveCaptionSafetyChecker(threshold=threshold)
    async for filtered in safety_checker.filter_unsafe_captions_async(caption_stream):
        yield filtered


def check_caption_safety(
    caption_stream: Generator[Dict[str, Any], None, None], threshold: float = 0.7
) -> Generator[Dict[str, Any], None, None]:

    return create_safety_filter_pipeline(caption_stream, threshold)


def analyze_caption_safety(text: str, threshold: float = 0.7) -> Dict[str, Any]:
    checker = LiveCaptionSafetyChecker(threshold=threshold)
    is_unsafe, analysis = checker.is_unsafe(text)
    return analysis
