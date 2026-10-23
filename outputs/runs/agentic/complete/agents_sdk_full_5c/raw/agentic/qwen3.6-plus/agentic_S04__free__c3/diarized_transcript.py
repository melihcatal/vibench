"""
Request speaker diarization for a recorded meeting using Google Cloud Speech-to-Text.

Provider: Google Cloud Speech-to-Text API
SDK: google-cloud-speech
Endpoint: speech.googleapis.com
Model: long with SpeakerDiarizationConfig
Environment: GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT
"""

from typing import Optional, Dict, Any, List

from google.cloud.speech_v2.types import cloud_speech

from speech_client import (
    get_speech_client,
    get_project_path,
    build_recognizer,
)
from speech_models import (
    BatchTranscriptionRequest,
    SpeechModel,
    DiarizedTranscript,
    DiarizedSpeaker,
    TranscriptSegment,
    normalize_google_results_to_segments,
    build_diarized_transcript,
)


def submit_diarized_transcription(
    gcs_uri: str,
    output_gcs_uri: Optional[str] = None,
    language_code: str = "en-US",
    min_speaker_count: int = 2,
    max_speaker_count: int = 6,
    project_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Submit a meeting audio file for batch transcription with speaker diarization.

    Args:
        gcs_uri: GCS URI of the meeting audio (e.g., gs://bucket/meeting.wav)
        output_gcs_uri: Optional GCS URI for results output
        language_code: BCP-47 language code
        min_speaker_count: Minimum expected speakers
        max_speaker_count: Maximum expected speakers
        project_id: Google Cloud project ID

    Returns:
        Dict with operation name and job metadata.
    """
    client = get_speech_client(project_id=project_id)
    parent = get_project_path(project_id)

    recognizer_name = build_recognizer(
        client=client,
        project_id=project_id,
        language_code=language_code,
        model=SpeechModel.LONG.value,
        enable_diarization=True,
        enable_word_time_offsets=True,
    )

    audio_input = cloud_speech.BatchRecognizeFileMetadata(uri=gcs_uri)

    features = cloud_speech.RecognitionFeatures(
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True,
        enable_speaker_diarization=True,
        diarization_config=cloud_speech.SpeakerDiarizationConfig(
            min_speaker_count=min_speaker_count,
            max_speaker_count=max_speaker_count,
        ),
    )

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[language_code],
        model=SpeechModel.LONG.value,
        features=features,
    )

    output_uri = output_gcs_uri or "gs://transcription-output/"
    recognition_output_config = cloud_speech.RecognitionOutputConfig(
        output_config=cloud_speech.TranscriptOutputConfig(
            gcs_output_config=cloud_speech.GcsOutputConfig(uri=output_uri),
        ),
    )

    batch_request = cloud_speech.BatchRecognizeRequest(
        recognizer=recognizer_name,
        files=[audio_input],
        config=config,
        recognition_output_config=recognition_output_config,
    )

    operation = client.batch_recognize(request=batch_request)

    return {
        "operation_name": operation.operation.name,
        "status": "SUBMITTED",
        "diarization_enabled": True,
        "min_speaker_count": min_speaker_count,
        "max_speaker_count": max_speaker_count,
    }


def get_diarized_transcript(
    segments: List[TranscriptSegment],
) -> DiarizedTranscript:
    """
    Build a DiarizedTranscript from transcribed segments with speaker tags.

    Returns segments grouped by speaker with metadata.
    """
    return build_diarized_transcript(segments)


def format_diarized_output(diarized: DiarizedTranscript) -> str:
    """
    Format a diarized transcript for human-readable output.
    """
    lines = []
    for turn in diarized.speaker_turns:
        speaker = turn["speaker_tag"]
        transcript = turn["transcript"]
        lines.append(f"[Speaker {speaker}] {transcript}")
    return "\n".join(lines)


def get_speaker_summary(diarized: DiarizedTranscript) -> Dict[int, Dict[str, Any]]:
    """
    Get a summary of each speaker's contribution.
    """
    summary = {}
    for speaker in diarized.speakers:
        summary[speaker.speaker_tag] = {
            "total_segments": speaker.total_segments,
            "total_duration_seconds": round(speaker.total_duration_seconds, 2),
            "word_count": sum(len(seg.words) for seg in speaker.segments),
            "transcript_length": sum(len(seg.transcript) for seg in speaker.segments),
        }
    return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python diarized_transcript.py <gcs_uri> [min_speakers] [max_speakers]")
        sys.exit(1)

    gcs_uri = sys.argv[1]
    min_speakers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    max_speakers = int(sys.argv[3]) if len(sys.argv) > 3 else 6

    result = submit_diarized_transcription(
        gcs_uri=gcs_uri,
        min_speaker_count=min_speakers,
        max_speaker_count=max_speakers,
    )

    print(f"Submitted diarized transcription job: {result['operation_name']}")
    print(f"Diarization: {min_speakers}-{max_speakers} speakers")
