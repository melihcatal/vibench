import json
import os
from typing import List, Dict, Any
from messaging_client import get_comprehend_client
from messaging_models import SummaryRequest

def summarize_message(summary_request: SummaryRequest) -> Dict[str, Any]:
    """Summarizes message content by extracting key phrases using AWS Comprehend.

    Args:
        summary_request: An instance of SummaryRequest containing the text and language code.

    Returns:
        A dictionary containing the detected key phrases and their scores.
    """
    comprehend_client = get_comprehend_client()

    try:
        response = comprehend_client.detect_key_phrases(
            Text=summary_request.text,
            LanguageCode=summary_request.language_code
        )
        return response
    except Exception as e:
        print(f"Error summarizing message with AWS Comprehend: {e}")
        raise

if __name__ == '__main__':
    # Example Usage (requires AWS credentials and AWS_REGION environment variable)
    # export AWS_REGION="us-east-1"

    sample_text = (
        "Amazon.com, Inc. is an American multinational technology company focusing on e-commerce, cloud computing, "
        "online advertising, digital streaming, and artificial intelligence. It has been referred to as \"one of the most "
        "influential economic and cultural forces in the world\"."
    )
    summary_req = SummaryRequest(text=sample_text, language_code="en")

    print(f"Analyzing text for key phrases:\n\"\"\"\n{summary_req.text}\n\"\"\"")
    try:
        summary_result = summarize_message(summary_req)
        print("Key Phrases:")
        for phrase in summary_result.get('KeyPhrases', []):
            print(f"- {phrase['Text']} (Score: {phrase['Score']:.2f})")
    except Exception as e:
        print(f"Failed to summarize message: {e}")
