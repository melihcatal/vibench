"""
Submit an audio file for batch transcription using Google Cloud Speech-to-Text.

Provider: Google Cloud Speech-to-Text API
SDK: google-cloud-speech
Endpoint: speech.googleapis.com
Model: long (for audio > 60 seconds)
Environment: GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT
"""

import os
from typing import Optional

from google.cloud.speech_v2.types import cloud_speech

from speech_client import (
    get_speech_client,
    get_project_path,
    build_recognizer,
    build_audio_input_from_gcs,
    wait_for_operation,
)
from speech_models import BatchTranscriptionRequest, SpeechModel


def submit_batch_transcription(
    gcs_uri: str,
    output_gcs_uri: Optional[str] = None,
    language_code: str = "en-US",
    model: SpeechModel = SpeechModel.LONG,
    project_id: Optional[str] = None,
) -> str:
    """
    Submit an audio file stored in Google Cloud Storage for batch transcription.

    Args:
        gcs_uri: GCS URI of the audio file (e.g., gs://bucket/audio.wav)
        output_gcs_uri: Optional GCS URI for transcription results output
        language_code: BCP-47 language code (default: en-US)
        model: Google Speech-to-Text model to use (default: long)
        project_id: Google Cloud project ID

    Returns:
        The operation name for the batch recognition job.
    """
    client = get_speech_client(project_id=project_id)
    parent = get_project_path(project_id)

    recognizer_name = build_recognizer(
        client=client,
        project_id=project_id,
        language_code=language_code,
        model=model.value,
    )

    audio_input = build_audio_input_from_gcs(gcs_uri)

    recognition_output_config = cloud_speech.RecognitionOutputConfig(
        output_config=cloud_speech.TranscriptOutputConfig(
            gcs_output_config=cloud_speech.GcsOutputConfig(
                uri=output_gcs_uri or f"gs://{os.environ.get('GCS_OUTPUT_BUCKET', 'transcription-output')}/",
            ),
        ),
    )

    batch_request = cloud_speech.BatchRecognizeRequest(
        recognizer=recognizer_name,
        files=[audio_input],
        recognition_output_config=recognition_output_config,
        config=cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=[language_code],
        ),
    )

    operation = client.batch_recognize(request=batch_request)

    return operation.operation.name


def submit_transcription_job(
    request: BatchTranscriptionRequest,
    project_id: Optional[str] = None,
) -> dict:
    """
    Submit a batch transcription job from a BatchTranscriptionRequest model.

    Returns a dict with operation_name and status.
    """
    client = get_speech_client(project_id=project_id)
    parent = get_project_path(project_id)

    recognizer_name = build_recognizer(
        client=client,
        project_id=project_id,
        language_code=request.language_code,
        model=request.model.value,
        enable_diarization=request.enable_diarization,
        enable_word_time_offsets=request.enable_word_time_offsets,
    )

    audio_input = cloud_speech.BatchRecognizeFileMetadata(
        uri=request.gcs_uri,
    )

    features = cloud_speech.RecognitionFeatures(
        enable_automatic_punctuation=True,
        enable_word_time_offsets=request.enable_word_time_offsets,
    )

    if request.enable_diarization:
        features.enable_speaker_diarization = True
        features.diarization_config = cloud_speech.SpeakerDiarizationConfig(
            min_speaker_count=request.min_speaker_count,
            max_speaker_count=request.max_speaker_count,
        )

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=[request.language_code],
        model=request.model.value,
        features=features,
    )

    output_uri = request.output_gcs_uri or f"gs://{os.environ.get('GCS_OUTPUT_BUCKET', 'transcription-output')}/"
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
        "gcs_uri": request.gcs_uri,
        "model": request.model.value,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python submit_transcription.py <gcs_uri> [output_gcs_uri]")
        sys.exit(1)

    gcs_uri = sys.argv[1]
    output_uri = sys.argv[2] if len(sys.argv) > 2 else None

    request = BatchTranscriptionRequest(
        gcs_uri=gcs_uri,
        output_gcs_uri=output_uri,
        model=SpeechModel.LONG,
        enable_diarization=True,
        enable_word_time_offsets=True,
    )

    result = submit_transcription_job(request)
    print(f"Submitted transcription job: {result['operation_name']}")
    print(f"Status: {result['status']}")
