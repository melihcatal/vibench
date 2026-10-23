from google.cloud import language_v1
from speech_models import TranscriptResult

class LiveCaptionSafetyChecker:
    def __init__(self):
        self.client = language_v1.LanguageServiceClient()

    def check_safety(self, caption: TranscriptResult) -> dict:
        if not caption.text.strip():
            return {"safe": True, "categories": []}

        document = language_v1.Document(content=caption.text, type_=language_v1.Document.Type.PLAIN_TEXT)

        # Classify text content
        response = self.client.classify_text(request={'document': document})
        
        safety_results = {"safe": True, "categories": []}
        # Threshold for flagging content as potentially unsafe (example: 0.7 confidence)
        UNSAFE_THRESHOLD = 0.7

        for category in response.categories:
            # Google NLU categories often start with '/'. We can simplify or map them.
            category_name = category.name.lstrip('/')
            
            # Example: Check for specific categories that might indicate unsafe content
            if category_name.startswith("Violence") or category_name.startswith("Sexual") or category_name.startswith("Hate Speech"):
                if category.confidence > UNSAFE_THRESHOLD:
                    safety_results["safe"] = False
                    safety_results["categories"].append({"name": category_name, "confidence": category.confidence})
            
            # Add all categories for more detailed analysis if needed
            # safety_results["categories"].append({"name": category_name, "confidence": category.confidence})

        print(f"Content: \" {caption.text} \" Safety Check: {safety_results}")
        return safety_results

if __name__ == "__main__":
    # Example usage
    safety_checker = LiveCaptionSafetyChecker()
    sample_caption_safe = TranscriptResult(text="This is a normal conversation.", is_partial=False)
    safety_checker.check_safety(sample_caption_safe)

    sample_caption_unsafe = TranscriptResult(text="I will hurt you.", is_partial=False)
    safety_checker.check_safety(sample_caption_unsafe)

    sample_caption_another_unsafe = TranscriptResult(text="This is hate speech.", is_partial=False)
    safety_checker.check_safety(sample_caption_another_unsafe)
