import boto3
import json
from datetime import datetime
from botocore.exceptions import ClientError
from speech_models import TranscriptionResult


def archive_summary(transcript_result: TranscriptionResult) -> dict:
    """
    Summarize transcription results using AWS Comprehend and archive to S3.

    Args:
        transcript_result: TranscriptionResult object

    Returns:
        Dictionary containing summary and archive information
    """
    # Create AWS Comprehend client for summarization
    comprehend_client = boto3.client(
        "comprehend",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    # Create S3 client for archiving
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        # Generate summary using AWS Comprehend (key phrases extraction)
        key_phrases_response = comprehend_client.detect_key_phrases(
            Text=transcript_result.transcript, LanguageCode="en"
        )

        # Extract top key phrases as summary
        key_phrases = []
        for phrase in key_phrases_response.get("KeyPhrases", []):
            key_phrases.append({"text": phrase["Text"], "score": phrase["Score"]})

        # Sort by score and take top 5
        top_key_phrases = sorted(key_phrases, key=lambda x: x["score"], reverse=True)[
            :5
        ]

        # Detect entities for better understanding
        entities_response = comprehend_client.detect_entities(
            Text=transcript_result.transcript, LanguageCode="en"
        )

        # Categorize entities
        entity_categories = {}
        for entity in entities_response.get("Entities", []):
            category = entity["Type"]
            if category not in entity_categories:
                entity_categories[category] = []
            entity_categories[category].append(
                {"text": entity["Text"], "score": entity["Score"]}
            )

        # Calculate metrics
        from speech_models import calculate_transcript_metrics

        metrics = calculate_transcript_metrics(
            transcript_result.transcript, transcript_result.items
        )

        # Create summary object
        summary = {
            "job_id": transcript_result.job_id,
            "timestamp": datetime.now().isoformat(),
            "word_count": metrics["word_count"],
            "duration_seconds": metrics["duration_seconds"],
            "average_confidence": metrics["average_confidence"],
            "key_topics": [phrase["text"] for phrase in top_key_phrases],
            "entity_categories": entity_categories,
            "speaker_count": len(
                set(
                    [
                        label["speaker_label"]
                        for label in transcript_result.speaker_labels
                    ]
                )
            )
            if transcript_result.speaker_labels
            else 1,
        }

        # Archive to S3
        bucket_name = os.environ.get(
            "AWS_TRANSCRIPT_ARCHIVE_BUCKET", "transcript-archive-bucket"
        )
        archive_key = f"summaries/{transcript_result.job_id}/summary.json"

        # Create archive data
        archive_data = {
            "summary": summary,
            "transcript_preview": transcript_result.transcript[:500] + "..."
            if len(transcript_result.transcript) > 500
            else transcript_result.transcript,
            "full_transcript_available": True,
            "archive_timestamp": datetime.now().isoformat(),
        }

        # Upload to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=archive_key,
            Body=json.dumps(archive_data, indent=2),
            ContentType="application/json",
        )

        # Also archive the full transcript
        transcript_key = f"transcripts/{transcript_result.job_id}/full_transcript.json"
        transcript_data = {
            "job_id": transcript_result.job_id,
            "transcript": transcript_result.transcript,
            "items": transcript_result.items,
            "speaker_labels": transcript_result.speaker_labels,
            "created_at": transcript_result.created_at.isoformat()
            if transcript_result.created_at
            else None,
            "archived_at": datetime.now().isoformat(),
        }

        s3_client.put_object(
            Bucket=bucket_name,
            Key=transcript_key,
            Body=json.dumps(transcript_data, indent=2),
            ContentType="application/json",
        )

        return {
            "job_id": transcript_result.job_id,
            "summary": summary,
            "archive_location": f"s3://{bucket_name}/{archive_key}",
            "transcript_archive_location": f"s3://{bucket_name}/{transcript_key}",
            "summary_service": "aws_comprehend",
            "archive_service": "aws_s3",
        }

    except ClientError as e:
        print(f"Error creating summary and archive: {e}")
        raise


import os
