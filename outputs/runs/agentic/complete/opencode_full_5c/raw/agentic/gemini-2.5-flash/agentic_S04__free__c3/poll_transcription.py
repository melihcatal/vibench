from speech_client import get_speech_client
from speech_models import TranscriptionResult, TranscriptionSegment
from google.api_core.operation import Operation
from google.cloud.speech_v1p1beta1 import LongRunningRecognizeResponse


def poll_transcription_result(operation_id: str) -> TranscriptionResult:
    """Polls a transcription job and returns the transcript."""
    client = get_speech_client()
    operation = Operation(operation_id, client=client)

    print(f"Polling transcription operation: {operation_id}")
    response: LongRunningRecognizeResponse = operation.result(
        timeout=600
    )  # Wait for up to 10 minutes

    full_transcript_text = []
    segments = []

    for result in response.results:
        if result.alternatives:
            alternative = result.alternatives[0]
            full_transcript_text.append(alternative.transcript)

            # Extract segments with speaker tags and word timestamps if available
            for word_info in alternative.words:
                start_time = (
                    word_info.start_time.seconds + word_info.start_time.nanos * 1e-9
                )
                end_time = word_info.end_time.seconds + word_info.end_time.nanos * 1e-9
                # For simplicity, each word becomes a segment here. More sophisticated segmentation might be needed.
                segments.append(
                    TranscriptionSegment(
                        start_time=start_time,
                        end_time=end_time,
                        text=word_info.word,
                        speaker_tag=word_info.speaker_tag
                        if hasattr(word_info, "speaker_tag")
                        else None,
                        word_timestamps=[
                            {
                                "word": word_info.word,
                                "start_time": start_time,
                                "end_time": end_time,
                            }
                        ],
                    )
                )

    return TranscriptionResult(
        operation_id=operation_id,
        transcript_text=" ".join(full_transcript_text),
        segments=segments,
    )
