import os
import time

from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError

from speech_client import get_speech_client
from speech_models import TranscriptionConfig, TranscriptionResult

def request_diarized_transcript(audio_uri: str, language_code: str = "en-US", speaker_count: int = 2) -> TranscriptionResult:
    """Requests a transcription with speaker diarization for a recorded meeting.

    Args:
        audio_uri: The Google Cloud Storage URI of the audio file.
        language_code: The language of the audio file.
        speaker_count: The estimated number of speakers in the audio.

    Returns:
        A TranscriptionResult object containing the full transcript and speaker segments.
    """
    client = get_speech_client()

    config_obj = TranscriptionConfig(
        audio_uri=audio_uri,
        language_code=language_code,
        enable_speaker_diarization=True,
        diarization_speaker_count=speaker_count
    )
    config = config_obj.to_recognition_config()
    audio = config_obj.to_recognition_audio()

    try:
        # Google Cloud Speech-to-Text API Call
        # Speaker diarization is enabled via config["diarization_config"]
        operation = client.long_running_recognize(config=config, audio=audio)
        print(f"Diarization transcription job submitted. Operation name: {operation.operation.name}")

        # Poll the operation for completion (reusing logic, but in a self-contained way for this file)
        start_time = time.time()
        timeout_seconds = 600
        while not operation.done:
            if time.time() - start_time > timeout_seconds:
                raise TimeoutError("Diarization transcription job timed out.")
            print(f"Polling diarization job {operation.operation.name}... (elapsed: {int(time.time() - start_time)}s)")
            time.sleep(10)
            operation = client.operations_client.get_operation(name=operation.operation.name)

        if operation.error:
            raise GoogleAPIError(f"Diarization transcription job failed: {operation.error.message}")

        result = speech.LongRunningRecognizeResponse(operation.response).results

        full_transcript_parts = []
        speaker_segments = []

        # Process results to get diarization
        for r in result:
            # The first alternative is the most likely one for diarization
            alternative = r.alternatives[0]
            full_transcript_parts.append(alternative.transcript)

            for word_info in alternative.words:
                speaker_segments.append({
                    "word": word_info.word,
                    "speaker_tag": word_info.speaker_tag,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                })
        
        full_transcript = " ".join(full_transcript_parts)
        return TranscriptionResult(full_transcript=full_transcript, speaker_segments=speaker_segments)

    except GoogleAPIError as e:
        print(f"Error requesting diarized transcript: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    gcs_audio_uri = "gs://cloud-samples-data/speech/long_audio.flac" # Use a longer audio with multiple speakers for testing diarization
    try:
        diarized_result = request_diarized_transcript(gcs_audio_uri, speaker_count=2)
        print("Full Diarized Transcript:")
        current_speaker_tag = None
        current_speaker_words = []
        for segment in diarized_result.speaker_segments:
            if current_speaker_tag is None or segment["speaker_tag"] != current_speaker_tag:
                if current_speaker_words:
                    print(f"Speaker {current_speaker_tag}: {' '.join(current_speaker_words)}")
                current_speaker_tag = segment["speaker_tag"]
                current_speaker_words = [segment["word"]]
            else:
                current_speaker_words.append(segment["word"])
        if current_speaker_words:
            print(f"Speaker {current_speaker_tag}: {' '.join(current_speaker_words)}")

    except Exception as e:
        print(f"Failed to get diarized transcript: {e}")
