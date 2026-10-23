import boto3
import os

AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

def summarize_audit_events(event_text: str) -> dict:
    comprehend = boto3.client("comprehend", region_name=AWS_REGION)
    try:
        # Detect the dominant language to help Comprehend with better analysis
        language_detection_response = comprehend.detect_dominant_language(Text=event_text)
        dominant_language = language_detection_response["Languages"][0]["LanguageCode"]

        # Use detect_key_phrases to extract key information as a form of summary
        key_phrases_response = comprehend.detect_key_phrases(
            Text=event_text,
            LanguageCode=dominant_language
        )
        key_phrases = [phrase["Text"] for phrase in key_phrases_response["KeyPhrases"]]
        
        return {"summary_phrases": key_phrases, "language": dominant_language}
    except Exception as e:
        return {"error": str(e)}
