from google.cloud import language_v1
from typing import Generator, Tuple, List, Dict, Any
import re


class LiveCaptionSafetyChecker:
    def __init__(self, credentials_path: Optional[str] = None):
        self.client = (
            language_v1.LanguageServiceClient.from_service_account_json(
                credentials_path
            )
            if credentials_path
            else language_v1.LanguageServiceClient()
        )
        self.profanity_patterns = [
            r"\b(ass|shit|fuck|damn|hell|bitch|bastard|crap)\b",
            r"\b(nigger|chink|spic|kike|fag|dyke)\b",
            r"\b(retard|moron|idiot|stupid)\b",
        ]
        self.profanity_regex = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.profanity_patterns
        ]

    def check_text_safety(self, text: str) -> Dict[str, Any]:
        if not text.strip():
            return {
                "is_safe": True,
                "profanity_found": False,
                "sentiment_score": 0.0,
                "sentiment_magnitude": 0.0,
                "categories": [],
                "offensive_words": [],
            }

        safety_result = {
            "is_safe": True,
            "profanity_found": False,
            "sentiment_score": 0.0,
            "sentiment_magnitude": 0.0,
            "categories": [],
            "offensive_words": [],
        }

        offensive_words = self._check_profanity(text)
        if offensive_words:
            safety_result["profanity_found"] = True
            safety_result["offensive_words"] = offensive_words
            safety_result["is_safe"] = False

        sentiment = self._analyze_sentiment(text)
        safety_result["sentiment_score"] = sentiment["score"]
        safety_result["sentiment_magnitude"] = sentiment["magnitude"]

        if sentiment["score"] < -0.5:
            safety_result["is_safe"] = False

        categories = self._classify_text(text)
        safety_result["categories"] = categories

        toxic_categories = {"HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT"}
        if any(cat in toxic_categories for cat in categories):
            safety_result["is_safe"] = False

        return safety_result

    def _check_profanity(self, text: str) -> List[str]:
        offensive_words = []
        text_lower = text.lower()

        for regex in self.profanity_regex:
            matches = regex.findall(text_lower)
            offensive_words.extend(matches)

        return list(set(offensive_words))

    def _analyze_sentiment(self, text: str) -> Dict[str, float]:
        try:
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT,
            )

            sentiment = self.client.analyze_sentiment(
                request={"document": document}
            ).document_sentiment

            return {"score": sentiment.score, "magnitude": sentiment.magnitude}
        except Exception as e:
            print(f"Sentiment analysis failed: {e}")
            return {"score": 0.0, "magnitude": 0.0}

    def _classify_text(self, text: str) -> List[str]:
        try:
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT,
            )

            response = self.client.classify_text(request={"document": document})

            categories = []
            for category in response.categories:
                categories.append(category.name)

            return categories
        except Exception as e:
            print(f"Text classification failed: {e}")
            return []

    def stream_safety_check(
        self, caption_stream: Generator[Tuple[str, bool], None, None]
    ) -> Generator[Tuple[str, bool, Dict[str, Any]], None, None]:

        for caption, is_final in caption_stream:
            if not caption.strip():
                continue

            safety_result = self.check_text_safety(caption)
            yield caption, is_final, safety_result

    def filter_unsafe_captions(
        self,
        caption_stream: Generator[Tuple[str, bool], None, None],
        replace_with: str = "[Content Removed]",
    ) -> Generator[Tuple[str, bool], None, None]:

        for caption, is_final, safety_result in self.stream_safety_check(
            caption_stream
        ):
            if not safety_result["is_safe"]:
                caption = replace_with

            yield caption, is_final


class ContentModerationPipeline:
    def __init__(self, credentials_path: Optional[str] = None):
        self.safety_checker = LiveCaptionSafetyChecker(credentials_path)
        self.flagged_content = []

    def moderate_stream(
        self,
        caption_stream: Generator[Tuple[str, bool], None, None],
        action: str = "filter",
    ) -> Generator[Tuple[str, bool, Dict[str, Any]], None, None]:

        for caption, is_final, safety_result in self.safety_checker.stream_safety_check(
            caption_stream
        ):
            if not safety_result["is_safe"]:
                self.flagged_content.append(
                    {
                        "text": caption,
                        "safety_result": safety_result,
                        "timestamp": is_final,
                    }
                )

                if action == "filter":
                    caption = "[Moderated Content]"
                elif action == "blank":
                    caption = ""

            yield caption, is_final, safety_result

    def get_moderation_report(self) -> Dict[str, Any]:
        total_flagged = len(self.flagged_content)

        categories_found = set()
        for item in self.flagged_content:
            categories_found.update(item["safety_result"]["categories"])

        return {
            "total_flagged": total_flagged,
            "categories_found": list(categories_found),
            "flagged_items": self.flagged_content,
        }


def create_safe_caption_stream(
    caption_stream: Generator[Tuple[str, bool], None, None],
    credentials_path: Optional[str] = None,
) -> Generator[Tuple[str, bool], None, None]:

    safety_checker = LiveCaptionSafetyChecker(credentials_path)

    for caption, is_final in safety_checker.filter_unsafe_captions(caption_stream):
        yield caption, is_final


def check_batch_safety(
    captions: List[str], credentials_path: Optional[str] = None
) -> List[Dict[str, Any]]:

    safety_checker = LiveCaptionSafetyChecker(credentials_path)
    results = []

    for caption in captions:
        safety_result = safety_checker.check_text_safety(caption)
        results.append({"text": caption, "safety_result": safety_result})

    return results
