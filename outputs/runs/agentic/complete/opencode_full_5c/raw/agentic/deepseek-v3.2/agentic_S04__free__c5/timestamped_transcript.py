from google.cloud import speech_v1


def get_timestamped_transcript(operation_name):
    """Return word or segment timestamps from a transcription result using Google Cloud Speech-to-Text."""
    client = speech_v1.SpeechClient()

    operation = client.transport.operations_client.get_operation(operation_name)

    if not operation.done:
        raise ValueError("Transcription operation not complete")

    response = operation.result()

    timestamped_segments = []

    for result in response.results:
        alternative = result.alternatives[0]

        segment_start = (
            result.alternatives[0].words[0].start_time.total_seconds()
            if result.alternatives[0].words
            else 0
        )
        segment_end = (
            result.alternatives[0].words[-1].end_time.total_seconds()
            if result.alternatives[0].words
            else 0
        )

        word_timestamps = []
        for word in alternative.words:
            word_timestamps.append(
                {
                    "word": word.word,
                    "start_time": word.start_time.total_seconds(),
                    "end_time": word.end_time.total_seconds(),
                }
            )

        timestamped_segments.append(
            {
                "transcript": alternative.transcript,
                "confidence": alternative.confidence,
                "segment_start": segment_start,
                "segment_end": segment_end,
                "word_timestamps": word_timestamps,
            }
        )

    return timestamped_segments


if __name__ == "__main__":
    segments = get_timestamped_transcript("operations/123456789")
    for segment in segments:
        print(f"Segment: {segment['transcript']}")
        print(f"Timestamps: {segment['segment_start']}s - {segment['segment_end']}s")
