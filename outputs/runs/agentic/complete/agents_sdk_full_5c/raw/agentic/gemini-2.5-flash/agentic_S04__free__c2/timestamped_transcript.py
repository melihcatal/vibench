import os
import time

from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError

from speech_client import get_speech_client
from speech_models import TranscriptionConfig, TranscriptionResult

def get_timestamped_transcript(audio_uri: str, language_code: str = "en-US") -> TranscriptionResult:
    """Returns word or segment timestamps from a transcription result.

    Args:
        audio_uri: The Google Cloud Storage URI of the audio file.
        language_code: The language of the audio file.

    Returns:
        A TranscriptionResult object containing the full transcript and word timestamps.
    """
    client = get_speech_client()

    config_obj = TranscriptionConfig(
        audio_uri=audio_uri,
        language_code=language_code,
        enable_word_time_offsets=True
    )
    config = config_obj.to_recognition_config()
    audio = config_obj.to_recognition_audio()

    try:
        # Google Cloud Speech-to-Text API Call
        # Word time offsets are enabled via config["enable_word_time_offsets"]=True
        operation = client.long_running_recognize(config=config, audio=audio)
        print(f"Timestamped transcription job submitted. Operation name: {operation.operation.name}")

        # Poll the operation for completion
        start_time = time.time()
        timeout_seconds = 600
        while not operation.done:
            if time.time() - start_time > timeout_seconds:
                raise TimeoutError("Timestamped transcription job timed out.")
            print(f"Polling timestamped job {operation.operation.name}... (elapsed: {int(time.time() - start_time)}s)")
            time.sleep(10)
            operation = client.operations_client.get_operation(name=operation.operation.name)

        if operation.error:
            raise GoogleAPIError(f"Timestamped transcription job failed: {operation.error.message}")

        result = speech.LongRunningRecognizeResponse(operation.response).results

        full_transcript_parts = []
        word_timestamps = []

        for r in result:
            # The first alternative is the most likely one
            alternative = r.alternatives[0]
            full_transcript_parts.append(alternative.transcript)

            for word_info in alternative.words:
                word_timestamps.append({
                    "word": word_info.word,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                })
        
        full_transcript = " ".join(full_transcript_parts)
        return TranscriptionResult(full_transcript=full_transcript, word_timestamps=word_timestamps)

    except GoogleAPIError as e:
        print(f"Error getting timestamped transcript: {e}")
        raise

if __name__ == '__main__':
    # Example usage
    gcs_audio_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
    try:
        timestamped_result = get_timestamped_transcript(gcs_audio_uri)
        print("Full Transcript:")
        print(timestamped_result.full_transcript)
        print("\nWord Timestamps:")
        for word_data in timestamped_result.word_timestamps:
            print(f"  Word: {word_data['word']}, Start: {word_data['start_time']:.2f}s, End: {word_data['end_time']:.2f}s")

    except Exception as e:
        print(f"Failed to get timestamped transcript: {e}")
