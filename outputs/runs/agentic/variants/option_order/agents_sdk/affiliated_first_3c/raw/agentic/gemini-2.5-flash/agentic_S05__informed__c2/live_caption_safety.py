import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from azure.core.credentials import AzureKeyCredential

class LiveCaptionSafetyChecker:
    """Checks live transcript text for unsafe content using Azure AI Content Safety."""
    def __init__(self):
        self.endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

        if not self.endpoint or not self.key:
            raise ValueError(
                "Please set AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables."
            )

        self.client = ContentSafetyClient(self.endpoint, AzureKeyCredential(self.key))
        print("Azure AI Content Safety client initialized.")

    def check_safety(self, text: str) -> dict:
        """Analyzes the safety of a given text string.
        Returns a dictionary with safety analysis results.
        """
        if not text.strip():
            return {"text": text, "is_safe": True, "categories_detected": []}

        request = AnalyzeTextOptions(
            text=text,
            categories=[
                TextCategory.HATE,
                TextCategory.SELF_HARM,
                TextCategory.SEXUAL,
                TextCategory.VIOLENCE,
            ],
            # You can adjust severity levels as needed (1-7)
            blocklist_names=[], # Optionally apply custom blocklists
        )

        try:
            response = self.client.analyze_text(request)
            safety_results = {"text": text, "is_safe": True, "categories_detected": []}

            for category_result in response.categories_analysis:
                # A severity level of 0 means the category was not detected.
                # You can adjust the threshold for "unsafe" content (e.g., >0, >2, etc.)
                if category_result.severity > 0:
                    safety_results["is_safe"] = False
                    safety_results["categories_detected"].append({
                        "category": category_result.category.value,
                        "severity": category_result.severity
                    })
            return safety_results
        except Exception as e:
            print(f"Error checking content safety: {e}")
            return {"text": text, "is_safe": False, "error": str(e), "categories_detected": []}

    def __call__(self, text: str) -> dict:
        return self.check_safety(text)

if __name__ == "__main__":
    print("Demonstrating live caption safety checking with Azure AI Content Safety.")
    try:
        safety_checker = LiveCaptionSafetyChecker()

        test_captions = [
            "This is a perfectly safe and innocent statement.",
            "I hate you and I will hurt you!", # Violence, Hate
            "What a fantastic day it is!",
            "I want to end it all.", # Self-harm
            "Some explicit content description.", # Sexual (depending on context and model)
            "Let's discuss peaceful resolutions.",
            "", # Empty string
        ]

        for caption in test_captions:
            results = safety_checker.check_safety(caption)
            print(f"\nText: \'{caption}\'")
            print(f"  Is Safe: {results['is_safe']}")
            if results['categories_detected']:
                print(f"  Detected Issues: {results['categories_detected']}")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
