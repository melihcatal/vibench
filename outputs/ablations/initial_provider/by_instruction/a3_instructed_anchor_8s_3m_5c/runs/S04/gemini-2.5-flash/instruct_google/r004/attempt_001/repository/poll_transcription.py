from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionJob, TranscriptionResult, TranscriptionAlternative, WordInfo
import time

def poll_transcription(job: TranscriptionJob) -> TranscriptionResult:
    """Polls a transcription job and returns the transcript.

    Args:
        job: The TranscriptionJob object to poll.

    Returns:
        A TranscriptionResult object containing the transcription results.
    """
    client = get_speech_client()

    # Poll the operation until it's done
    operation = client.long_running_recognize(operation_name=job.name)
    
    while not operation.done():
        time.sleep(5)  # Wait for 5 seconds before polling again
        operation.refresh()

    response = operation.result()

    # Process the results
    alternatives = []
    for result in response.results:
        for alternative in result.alternatives:
            words = []
            if alternative.words:
                for word_info in alternative.words:
                    words.append(WordInfo(
                        start_time=f"{word_info.start_time.seconds}.{word_info.start_time.nanos // 1000000:03d}s",
                        end_time=f"{word_info.end_time.seconds}.{word_info.end_time.nanos // 1000000:03d}s",
                        word=word_info.word,
                        speaker_tag=word_info.speaker_tag if hasattr(word_info, 'speaker_tag') else None
                    ))

            alternatives.append(TranscriptionAlternative(
                transcript=alternative.transcript,
                confidence=alternative.confidence,
                words=words
            ))
    
    # Assuming the first result's language code and end time for the overall result
    result_end_time = f"{response.results[-1].result_end_time.seconds}.{response.results[-1].result_end_time.nanos // 1000000:03d}s"
    language_code = response.results[0].language_code if response.results else ""

    return TranscriptionResult(
        alternatives=alternatives,
        result_end_time=result_end_time,
        language_code=language_code
    )
