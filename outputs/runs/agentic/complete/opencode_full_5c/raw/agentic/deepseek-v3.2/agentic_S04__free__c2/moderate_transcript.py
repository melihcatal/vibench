import boto3
from botocore.exceptions import ClientError
from speech_models import TranscriptionResult


def moderate_transcript(transcript_result: TranscriptionResult) -> dict:
    """
    Moderate transcript text before publishing using AWS Comprehend.

    Args:
        transcript_result: TranscriptionResult object

    Returns:
        Dictionary containing moderation results
    """
    # Create AWS Comprehend client
    comprehend_client = boto3.client(
        "comprehend",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        # Detect PII entities
        pii_response = comprehend_client.detect_pii_entities(
            Text=transcript_result.transcript, LanguageCode="en"
        )

        # Detect toxic content
        toxicity_response = comprehend_client.detect_toxic_content(
            TextSegments=[{"Text": transcript_result.transcript}], LanguageCode="en"
        )

        # Detect sentiment
        sentiment_response = comprehend_client.detect_sentiment(
            Text=transcript_result.transcript, LanguageCode="en"
        )

        # Detect key phrases
        key_phrases_response = comprehend_client.detect_key_phrases(
            Text=transcript_result.transcript, LanguageCode="en"
        )

        # Process PII entities
        pii_entities = []
        for entity in pii_response.get("Entities", []):
            pii_entities.append(
                {
                    "type": entity["Type"],
                    "score": entity["Score"],
                    "text": transcript_result.transcript[
                        entity["BeginOffset"] : entity["EndOffset"]
                    ],
                }
            )

        # Process toxic content
        toxic_segments = []
        for result in toxicity_response.get("ResultList", []):
            for label in result.get("Labels", []):
                toxic_segments.append({"label": label["Name"], "score": label["Score"]})

        # Process key phrases
        key_phrases = []
        for phrase in key_phrases_response.get("KeyPhrases", []):
            key_phrases.append({"text": phrase["Text"], "score": phrase["Score"]})

        # Determine if transcript needs moderation
        needs_moderation = False
        moderation_reasons = []

        if pii_entities:
            needs_moderation = True
            moderation_reasons.append(
                "Contains PII (Personally Identifiable Information)"
            )

        if any(segment["score"] > 0.7 for segment in toxic_segments):
            needs_moderation = True
            moderation_reasons.append("Contains toxic content")

        # Create redacted transcript
        redacted_transcript = transcript_result.transcript
        for entity in sorted(pii_entities, key=lambda x: x["score"], reverse=True):
            if entity["score"] > 0.9:  # High confidence PII
                redacted_transcript = redacted_transcript.replace(
                    entity["text"], f"[REDACTED_{entity['type']}]"
                )

        return {
            "job_id": transcript_result.job_id,
            "needs_moderation": needs_moderation,
            "moderation_reasons": moderation_reasons,
            "sentiment": sentiment_response["Sentiment"],
            "sentiment_scores": sentiment_response["SentimentScore"],
            "pii_entities": pii_entities,
            "toxic_content": toxic_segments,
            "key_phrases": key_phrases,
            "redacted_transcript": redacted_transcript if needs_moderation else None,
            "moderation_service": "aws_comprehend",
        }

    except ClientError as e:
        print(f"Error moderating transcript: {e}")
        raise


import os
