from typing import Optional, Dict, Any, List, Generator
import asyncio
from google.cloud import language_v1


class LiveCaptionSafetyChecker:
    def __init__(self, credentials_path: Optional[str] = None, threshold: float = 0.7):

        self.threshold = threshold

        if credentials_path:
            self.client = language_v1.LanguageServiceClient.from_service_account_json(
                credentials_path
            )
        else:
            self.client = language_v1.LanguageServiceClient()

        self.safety_categories = {
            "TOXICITY": "Toxic content",
            "SEVERE_TOXICITY": "Severely toxic content",
            "IDENTITY_ATTACK": "Identity attack",
            "INSULT": "Insulting content",
            "PROFANITY": "Profanity",
            "THREAT": "Threatening content",
            "SEXUALLY_EXPLICIT": "Sexually explicit content",
            "FLIRTATION": "Flirtation",
        }

    def analyze_safety(
        self, text: str, categories: Optional[List[str]] = None
    ) -> Dict[str, Any]:

        if categories is None:
            categories = list(self.safety_categories.keys())

        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        try:
            response = self.client.analyze_sentiment(
                request={
                    "document": document,
                    "features": {
                        "extract_entities": True,
                        "extract_document_sentiment": True,
                        "classify_text": False,
                    },
                }
            )

            sentiment_score = response.document_sentiment.score
            sentiment_magnitude = response.document_sentiment.magnitude

            safety_scores = {}
            for category in categories:
                if category in self.safety_categories:
                    safety_scores[category] = 0.0

            try:
                from google.cloud import language_v1beta2

                annotate_client = language_v1beta2.LanguageServiceClient()

                analyze_request = language_v1beta2.AnalyzeSentimentRequest(
                    document=language_v1beta2.Document(
                        content=text, type_=language_v1beta2.Document.Type.PLAIN_TEXT
                    ),
                    features=language_v1beta2.AnnotateTextRequest.Features(
                        extract_entity_sentiment=True, extract_document_sentiment=True
                    ),
                )

                response_beta = annotate_client.analyze_sentiment(analyze_request)

            except ImportError:
                pass

            entities = []
            for entity in response.entities:
                entities.append(
                    {
                        "name": entity.name,
                        "type": language_v1.Entity.Type(entity.type_).name,
                        "salience": entity.salience,
                        "sentiment_score": getattr(entity, "sentiment", {}).get(
                            "score", 0.0
                        ),
                    }
                )

            is_unsafe = any(score > self.threshold for score in safety_scores.values())

            return {
                "text": text,
                "sentiment_score": sentiment_score,
                "sentiment_magnitude": sentiment_magnitude,
                "safety_scores": safety_scores,
                "is_unsafe": is_unsafe,
                "unsafe_categories": [
                    cat
                    for cat, score in safety_scores.items()
                    if score > self.threshold
                ],
                "entities": entities,
                "language": "en",
            }

        except Exception as e:
            print(f"Safety analysis failed: {e}")
            return {
                "text": text,
                "error": str(e),
                "is_unsafe": False,
                "safety_scores": {},
                "sentiment_score": 0.0,
                "sentiment_magnitude": 0.0,
            }

    def check_caption_stream(
        self,
        caption_stream: Generator[Dict[str, Any], None, None],
        check_final_only: bool = True,
    ) -> Generator[Dict[str, Any], None, None]:

        for caption in caption_stream:
            if check_final_only and not caption.get("is_final", False):
                yield {**caption, "safety_checked": False, "safety_result": None}
                continue

            transcript = caption.get("transcript", "")
            if not transcript.strip():
                yield {**caption, "safety_checked": False, "safety_result": None}
                continue

            safety_result = self.analyze_safety(transcript)

            yield {
                **caption,
                "safety_checked": True,
                "safety_result": safety_result,
                "is_unsafe": safety_result.get("is_unsafe", False),
                "sentiment_score": safety_result.get("sentiment_score", 0.0),
                "unsafe_categories": safety_result.get("unsafe_categories", []),
            }

    async def check_caption_stream_async(
        self, caption_stream, check_final_only: bool = True
    ):

        async for caption in caption_stream:
            if check_final_only and not caption.get("is_final", False):
                yield {**caption, "safety_checked": False, "safety_result": None}
                continue

            transcript = caption.get("transcript", "")
            if not transcript.strip():
                yield {**caption, "safety_checked": False, "safety_result": None}
                continue

            loop = asyncio.get_event_loop()
            safety_result = await loop.run_in_executor(
                None, self.analyze_safety, transcript
            )

            yield {
                **caption,
                "safety_checked": True,
                "safety_result": safety_result,
                "is_unsafe": safety_result.get("is_unsafe", False),
                "sentiment_score": safety_result.get("sentiment_score", 0.0),
                "unsafe_categories": safety_result.get("unsafe_categories", []),
            }

    def get_safety_summary(
        self, safety_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        total_captions = len(safety_results)
        unsafe_captions = [r for r in safety_results if r.get("is_unsafe", False)]

        category_counts = {}
        for result in unsafe_captions:
            for category in result.get("unsafe_categories", []):
                category_counts[category] = category_counts.get(category, 0) + 1

        avg_sentiment = 0.0
        sentiment_results = [
            r.get("sentiment_score", 0.0)
            for r in safety_results
            if r.get("safety_checked", False)
        ]
        if sentiment_results:
            avg_sentiment = sum(sentiment_results) / len(sentiment_results)

        return {
            "total_captions": total_captions,
            "unsafe_captions": len(unsafe_captions),
            "safety_percentage": (len(unsafe_captions) / total_captions * 100)
            if total_captions > 0
            else 0,
            "unsafe_category_breakdown": category_counts,
            "average_sentiment": avg_sentiment,
            "most_common_unsafe_category": max(
                category_counts.items(), key=lambda x: x[1]
            )[0]
            if category_counts
            else None,
        }


class SafetyFilter:
    def __init__(
        self, safety_checker: LiveCaptionSafetyChecker, filter_unsafe: bool = True
    ):
        self.safety_checker = safety_checker
        self.filter_unsafe = filter_unsafe

    def filter_caption_stream(self, caption_stream):
        for caption in self.safety_checker.check_caption_stream(caption_stream):
            if self.filter_unsafe and caption.get("is_unsafe", False):
                unsafe_cats = caption.get("unsafe_categories", [])
                cat_names = [
                    self.safety_checker.safety_categories.get(cat, cat)
                    for cat in unsafe_cats
                ]

                filtered_caption = caption.copy()
                filtered_caption["transcript"] = (
                    f"[CONTENT FILTERED: {', '.join(cat_names)}]"
                )
                filtered_caption["filtered"] = True

                yield filtered_caption
            else:
                caption["filtered"] = False
                yield caption


def example_unsafe_caption_generator():
    captions = [
        {
            "transcript": "Good morning everyone.",
            "is_final": True,
            "language_code": "en",
        },
        {
            "transcript": "Let's begin with the project updates.",
            "is_final": True,
            "language_code": "en",
        },
        {
            "transcript": "This is absolutely terrible work!",
            "is_final": True,
            "language_code": "en",
        },
        {
            "transcript": "We need to improve our",
            "is_final": False,
            "language_code": "en",
        },
        {
            "transcript": "We need to improve our performance significantly.",
            "is_final": True,
            "language_code": "en",
        },
    ]

    for caption in captions:
        yield caption


if __name__ == "__main__":
    safety_checker = LiveCaptionSafetyChecker(threshold=0.6)

    caption_gen = example_unsafe_caption_generator()

    print("Starting live caption safety analysis:")
    print("=" * 60)

    for checked_caption in safety_checker.check_caption_stream(caption_gen):
        if checked_caption["safety_checked"]:
            print(f"Caption: {checked_caption['transcript']}")
            print(f"Sentiment: {checked_caption['sentiment_score']:.2f}")
            print(f"Unsafe: {checked_caption['is_unsafe']}")

            if checked_caption["is_unsafe"]:
                print(
                    f"Unsafe categories: {', '.join(checked_caption['unsafe_categories'])}"
                )

            print("-" * 40)
