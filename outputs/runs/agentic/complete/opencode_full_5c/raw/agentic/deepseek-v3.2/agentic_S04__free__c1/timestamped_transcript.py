from google.cloud import speech_v1
from google.api_core.operation import Operation


def get_timestamped_transcript(operation_name):
    """Return word or segment timestamps from a transcription result."""
    client = speech_v1.SpeechClient()

    operation = Operation.from_gapic(
        operation_name,
        client._transport.operations_client,
        speech_v1.types.LongRunningRecognizeResponse,
        metadata_type=speech_v1.types.LongRunningRecognizeMetadata,
    )

    if not operation.done():
        print(f"Transcription job {operation_name} is still processing...")
        return None

    response = operation.result()

    timestamped_segments = []

    for result in response.results:
        alternative = result.alternatives[0]

        segment = {
            "transcript": alternative.transcript,
            "start_time": result.alternatives[0].words[0].start_time.total_seconds()
            if alternative.words
            else 0,
            "end_time": result.alternatives[0].words[-1].end_time.total_seconds()
            if alternative.words
            else 0,
            "words": [],
        }

        if alternative.words:
            for word_info in alternative.words:
                segment["words"].append(
                    {
                        "word": word_info.word,
                        "start_time": word_info.start_time.total_seconds(),
                        "end_time": word_info.end_time.total_seconds(),
                    }
                )

        timestamped_segments.append(segment)

    return timestamped_segments
