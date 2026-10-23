from google.cloud import language_v2
from speech_models import SpeechRecognitionResult
from typing import Iterator, Dict, Any

class SafetyChecker:
    def __init__(self):
        self._client = language_v2.LanguageServiceClient()

    def check_safety(self, caption: SpeechRecognitionResult) -> Dict[str, Any]:
        if not caption.text:
            return {"text": caption.text, "is_safe": True, "categories": []}

        # Google Cloud Natural Language API for content moderation
        document = language_v2.Document(content=caption.text, type_=language_v2.Document.Type.PLAIN_TEXT)
        response = self._client.moderate_text(document=document)

        # Process the moderation response
        is_safe = True
        categories = []
        for category in response.moderation_categories:
            # The API returns scores between 0 and 1. A higher score means more likely to be in that category.
            # We can define a threshold for what's considered "unsafe".
            # For simplicity, let's just list categories with a score above 0.5
            if category.score > 0.5:
                is_safe = False
                categories.append({"name": category.name, "score": category.score})
        
        return {"text": caption.text, "is_safe": is_safe, "categories": categories, "is_final": caption.is_final}

def live_caption_safety(captions: Iterator[SpeechRecognitionResult]) -> Iterator[Dict[str, Any]]:
    safety_checker = SafetyChecker()
    for caption in captions:
        yield safety_checker.check_safety(caption)
