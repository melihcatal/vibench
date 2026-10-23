from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
import time

def get_timestamped_transcript(gcs_uri: str, language_code: str = "en-US"):
    """
    Returns word or segment timestamps from a transcription result using Google Cloud Speech-to-Text.
    """
    client = speech.SpeechClient()

    audio = speech.types.RecognitionAudio(uri=gcs_uri)
    config = speech.types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16, # Example, adjust based on actual audio
        sample_rate_hertz=16000, # Example, adjust based on actual audio
        language_code=language_code,
        enable_word_time_offsets=True, # Crucial for getting timestamps
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(request={"config": config, "audio": audio})
    print(f"Timestamped transcription operation submitted: {operation.operation.name}")

    # Poll the operation for completion (similar to poll_transcription.py)
    while not operation.done:
        print("Timestamped transcription job not yet complete, waiting...")
        time.sleep(5)  # Wait for 5 seconds before polling again
        operation = client.get_operation(name=operation.operation.name)

    if operation.error:
        print(f"Timestamped transcription job failed: {operation.error}")
        return None
    else:
        response = speech.types.LongRunningRecognizeResponse(operation.response)
        timestamps = []
        for result in response.results:
            for word_info in result.alternatives[0].words:
                timestamps.append({
                    "word": word_info.word,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                })
        print("Timestamped transcription job completed.")
        return timestamps
