import boto3
from botocore.exceptions import ClientError
from speech_models import TranscriptionResult


def translate_transcript(
    transcript_result: TranscriptionResult, target_language: str = "es"
) -> dict:
    """
    Translate completed transcript segments using AWS Translate.

    Args:
        transcript_result: TranscriptionResult object
        target_language: Target language code (default: Spanish)

    Returns:
        Dictionary containing translated transcript
    """
    # Create AWS Translate client
    translate_client = boto3.client(
        "translate",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )

    try:
        # Translate the full transcript
        response = translate_client.translate_text(
            Text=transcript_result.transcript,
            SourceLanguageCode="en",
            TargetLanguageCode=target_language,
        )

        translated_text = response["TranslatedText"]

        # Translate segment timestamps if available
        translated_segments = []

        # Import timestamped_transcript to get segment information
        from timestamped_transcript import timestamped_transcript

        try:
            timestamped = timestamped_transcript(transcript_result.job_id)

            for segment in timestamped.segment_timestamps:
                segment_response = translate_client.translate_text(
                    Text=segment["text"],
                    SourceLanguageCode="en",
                    TargetLanguageCode=target_language,
                )

                translated_segments.append(
                    {
                        "original_text": segment["text"],
                        "translated_text": segment_response["TranslatedText"],
                        "start_time": segment["start_time"],
                        "end_time": segment["end_time"],
                        "speaker_label": segment.get("speaker_label", "spk_0"),
                    }
                )
        except Exception as e:
            print(f"Note: Could not translate segments: {e}")

        return {
            "job_id": transcript_result.job_id,
            "original_transcript": transcript_result.transcript,
            "translated_transcript": translated_text,
            "target_language": target_language,
            "source_language": "en",
            "translated_segments": translated_segments,
            "translation_service": "aws_translate",
        }

    except ClientError as e:
        print(f"Error translating transcript: {e}")
        raise


import os
