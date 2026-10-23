import os

import boto3


def summarize_document_text(text):
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    comprehend = boto3.client("comprehend", region_name=region_name)

    # For summarization, Comprehend doesn't have a direct 'summarize' API.
    # A common approach is to detect key phrases or entities to get a summary idea.
    # For true summarization, often a more advanced NLP service or custom model is used.
    # Here, we'll use detect_key_phrases as a proxy for identifying key aspects.
    response = comprehend.detect_key_phrases(Text=text, LanguageCode="en")
    key_phrases = [phrase["Text"] for phrase in response["KeyPhrases"]]

    return {"summary_phrases": key_phrases}
