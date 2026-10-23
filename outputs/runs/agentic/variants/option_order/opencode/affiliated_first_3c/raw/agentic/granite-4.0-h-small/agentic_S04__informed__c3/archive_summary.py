# LATER-STEP summarize completed transcript using Granite model via watsonx.ai
import os
import requests
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Configure Watsonx Natural Language Understanding (Granite model)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
authenticator = IAMAuthenticator(WATSONX_API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version="2024-08-01",
    service_url="https://api.us-south.nlu.watson.cloud.ibm.com",
    authenticator=authenticator,
)


def summarize_transcript(transcript_text: str, max_words: int = 100) -> str:
    """Generate a concise summary of a transcript using Granite.

    Args:
        transcript_text (str): Full transcript.
        max_words (int): Approximate word count for the summary.

    Returns:
        str: Summary text.
    """
    response = nlu.summarize(
        text=transcript_text,
        content_type="text/plain",
        max_sentences=max_words // 20,  # heuristic
    ).get_result()
    return response["summaries"][0]["text"]


# Simple CLI example
if __name__ == "__main__":
    import sys

    transcript = sys.stdin.read()
    if not transcript:
        raise RuntimeError("No transcript supplied via stdin")
    summary = summarize_transcript(transcript)
    print("=== Summary ===\n", summary)
