from speech_client import get_speech_client
from speech_models import TranscriptionResult, WordInfo
from google.cloud import speech_v1p1beta1 as speech

def get_timestamped_transcript(operation_name: str) -> TranscriptionResult | None:
    """Retrieves a transcription job result with word-level timestamps.

    Args:
        operation_name: The name of the long-running operation.

    Returns:
        A TranscriptionResult object with transcript and word timestamps if the
        operation is complete, otherwise None.
    """
    client = get_speech_client()
    operation = client.operations.get(name=operation_name)

    if operation.done:
        response = speech.LongRunningRecognizeResponse(operation.result)
        
        full_transcript = []
        word_info_list = []

        for result in response.results:
            full_transcript.append(result.alternatives[0].transcript)
            for word_info in result.alternatives[0].words:
                word_info_list.append(WordInfo(
                    word=word_info.word,
                    start_time=word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    end_time=word_info.end_time.seconds + word_info.end_time.nanos * 1e-9
                ))
        
        return TranscriptionResult(transcript="".join(full_transcript), words=word_info_list)
    return None
