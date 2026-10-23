"""
Transcribe synthesized QA samples to verify spoken output using Amazon Transcribe.

This module converts synthesized TTS audio back to text using Amazon Transcribe
for quality assurance, enabling comparison between original input and spoken output.

Provider: Amazon Transcribe (transcribe.us-east-1.amazonaws.com)
Service: AWS Transcribe Streaming / Batch
"""

import os
import io
from typing import Optional
from pathlib import Path

import boto3
from botocore.config import Config

# Amazon Transcribe configuration
TRANSCRIBE_SERVICE_NAME = "transcribe"
TRANSCRIBE_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

# Supported media formats for Amazon Transcribe
SUPPORTED_MEDIA_FORMATS = ("mp3", "wav", "flac", "ogg")


class TranscribeClient:
    """Wrapper around boto3 Amazon Transcribe client."""

    def __init__(
        self,
        region_name: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        self.region = region_name or TRANSCRIBE_DEFAULT_REGION
        
        session_config = Config(
            retries={"max_attempts": 3, "mode": "standard"},
        )
        
        self.client = boto3.client(
            service_name=TRANSCRIBE_SERVICE_NAME,
            region_name=self.region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=session_config,
        )


def transcribe_audio_file(
    audio_path: str,
    language_code: str = "en-US",
    media_format: Optional[str] = None,
    client: Optional[TranscribeClient] = None,
) -> dict:
    """
    Transcribe an audio file using Amazon Transcribe batch transcription.
    
    Creates a transcription job for the audio file stored in S3 or local path.
    For local files, the file should be uploaded to S3 first.
    
    Args:
        audio_path: Path to audio file (local or S3 URI)
        language_code: BCP-47 language code (e.g., 'en-US', 'es-ES')
        media_format: Media format ('mp3', 'wav', 'flac', 'ogg')
        client: Optional pre-configured TranscribeClient
        
    Returns:
        Dict with transcription status and job details
    """
    if not client:
        client = TranscribeClient()
    
    # Determine media format from path if not provided
    if not media_format:
        ext = Path(audio_path).suffix.lower().lstrip(".")
        media_format = ext if ext in SUPPORTED_MEDIA_FORMATS else "mp3"
    
    # For local files, provide guidance; for S3 URIs, use directly
    if audio_path.startswith("s3://"):
        media_uri = audio_path
    else:
        # Local file needs to be uploaded to S3 first
        raise ValueError(
            "Local audio files must be uploaded to S3 before transcription. "
            "Provide an S3 URI (s3://bucket/key) or use streaming transcription."
        )
    
    import uuid
    job_name = f"tts-qa-{uuid.uuid4().hex[:8]}"
    
    response = client.client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat=media_format,
        Media={"MediaFileUri": media_uri},
        Settings={
            "ShowSpeakerLabels": False,
            "ShowAlternatives": True,
            "MaxAlternatives": 3,
        },
    )
    
    return {
        "job_name": job_name,
        "status": response["TranscriptionJob"]["TranscriptionJobStatus"],
        "language_code": language_code,
        "media_format": media_format,
    }


def transcribe_qa_sample(
    audio_bytes: bytes,
    original_text: str,
    language_code: str = "en-US",
    client: Optional[TranscribeClient] = None,
) -> dict:
    """
    Transcribe a QA audio sample and compare with original text.
    
    This function uses Amazon Transcribe to verify TTS output quality
    by comparing the transcribed result with the original input text.
    
    Args:
        audio_bytes: Audio bytes from TTS synthesis
        original_text: Original text that was synthesized
        language_code: Language code for transcription
        client: Optional TranscribeClient
        
    Returns:
        Dict with QA comparison results
    """
    if not client:
        client = TranscribeClient()
    
    # Note: For actual production use, audio_bytes would be uploaded to S3
    # and then transcribed. Here we return the structure for the workflow.
    # In practice, use Amazon Transcribe Streaming API for real-time verification.
    
    return {
        "original_text": original_text,
        "transcribed_text": None,  # Would be populated after S3 upload and job completion
        "language_code": language_code,
        "audio_length_bytes": len(audio_bytes),
        "status": "pending_s3_upload",
        "qa_match": None,
    }


def compare_transcript_to_original(
    transcribed: str,
    original: str,
    case_sensitive: bool = False,
    strip_punctuation: bool = True,
) -> dict:
    """
    Compare transcribed text to original TTS input for QA verification.
    
    Args:
        transcribed: Text from Amazon Transcribe
        original: Original text that was synthesized
        case_sensitive: Whether comparison is case-sensitive
        strip_punctuation: Remove punctuation before comparison
        
    Returns:
        Dict with comparison metrics
    """
    import string
    
    t = transcribed or ""
    o = original or ""
    
    if strip_punctuation:
        t = t.translate(str.maketrans("", "", string.punctuation))
        o = o.translate(str.maketrans("", "", string.punctuation))
    
    if not case_sensitive:
        t = t.lower()
        o = o.lower()
    
    t_words = t.split()
    o_words = o.split()
    
    # Word-level accuracy
    if not o_words:
        return {"match": True, "word_accuracy": 1.0, "exact_match": True}
    
    matches = sum(1 for tw, ow in zip(t_words, o_words) if tw == ow)
    word_accuracy = matches / max(len(o_words), len(t_words))
    
    exact_match = t.strip() == o.strip()
    
    return {
        "match": word_accuracy > 0.9,
        "exact_match": exact_match,
        "word_accuracy": word_accuracy,
        "original_word_count": len(o_words),
        "transcribed_word_count": len(t_words),
        "matching_words": matches,
    }


def get_transcription_job(job_name: str, client: Optional[TranscribeClient] = None) -> dict:
    """
    Get status of an Amazon Transcribe transcription job.
    
    Args:
        job_name: Name of the transcription job
        client: Optional TranscribeClient
        
    Returns:
        Dict with job status and results
    """
    if not client:
        client = TranscribeClient()
    
    response = client.client.get_transcription_job(TranscriptionJobName=job_name)
    job = response["TranscriptionJob"]
    
    result = {
        "job_name": job_name,
        "status": job["TranscriptionJobStatus"],
        "language_code": job.get("LanguageCode"),
    }
    
    if job["TranscriptionJobStatus"] == "COMPLETED":
        transcript_uri = job["Transcript"]["TranscriptFileUri"]
        result["transcript_uri"] = transcript_uri
    
    return result


if __name__ == "__main__":
    # Example QA workflow
    original = "This is a test of the Amazon Transcribe quality assurance process."
    
    print("QA Transcript Verification Example")
    print(f"Original text: {original}")
    print("\nTo complete QA transcription:")
    print("1. Upload TTS audio to S3")
    print("2. Call transcribe_audio_file() with S3 URI")
    print("3. Poll get_transcription_job() for completion")
    print("4. Use compare_transcript_to_original() to verify accuracy")
