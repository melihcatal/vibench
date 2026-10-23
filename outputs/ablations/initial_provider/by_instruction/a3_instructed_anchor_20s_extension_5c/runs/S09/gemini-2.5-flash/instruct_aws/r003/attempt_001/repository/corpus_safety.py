import boto3
import os
from typing import List, Dict

class ContentSafetyClient:
    def __init__(self, region_name=None):
        self.region_name = region_name or os.environ.get("AWS_REGION", "us-east-1")
        self.client = boto3.client("comprehend", region_name=self.region_name)

    def check_text_safety(self, text: str) -> Dict:
        """Checks a single text string for safety using AWS Comprehend.

        Args:
            text: The text string to check.

        Returns:
            A dictionary containing the sentiment and key phrases detected by Comprehend.
        """
        # Using detect_sentiment and detect_key_phrases as examples of safety/content analysis
        # For more explicit safety checks, AWS Rekognition for images or a custom solution with Comprehend
        # may be needed, but for text, sentiment and key phrases can indicate potential issues.
        sentiment_response = self.client.detect_sentiment(Text=text, LanguageCode='en')
        key_phrases_response = self.client.detect_key_phrases(Text=text, LanguageCode='en')

        return {
            "sentiment": sentiment_response,
            "key_phrases": key_phrases_response
        }

def corpus_safety(corpus_texts: List[str]) -> List[Dict]:
    """Checks a corpus of texts for safety using AWS Comprehend before embedding.

    Args:
        corpus_texts: A list of text strings representing the corpus.

    Returns:
        A list of dictionaries, each containing safety analysis results for the corresponding text.
    """
    safety_client = ContentSafetyClient()
    safety_results = []
    for text in corpus_texts:
        safety_results.append(safety_client.check_text_safety(text))
    return safety_results
