from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionResult, WordInfo, DiarizationSpeakerTag


def poll_transcription_job(operation_name: str) -> TranscriptionResult:
    client = get_speech_client()
    operation = client.long_running_recognize(operation_name=operation_name)

    print(f"Polling transcription job: {operation_name} (status: {operation.done})")

    if operation.done:
        response = operation.result
        full_transcript = []
        word_timestamps = []
        diarized_segments = []

        for result in response.results:
            full_transcript.append(result.alternatives[0].transcript)
            if result.alternatives[0].words:
                for word_info in result.alternatives[0].words:
                    word_timestamps.append(
                        WordInfo(
                            word=word_info.word,
                            start_time=word_info.start_time.total_seconds(),
                            end_time=word_info.end_time.total_seconds(),
                        )
                    )
            # Diarization results are typically aggregated per segment,
            # this example assumes simple processing for demonstration.
            # Real diarization parsing can be more complex.
            if result.alternatives[0].words and hasattr(
                result.alternatives[0].words[0], "speaker_tag"
            ):
                current_speaker_tag = None
                current_words = []
                for word_info in result.alternatives[0].words:
                    if current_speaker_tag is None:
                        current_speaker_tag = word_info.speaker_tag
                    if word_info.speaker_tag == current_speaker_tag:
                        current_words.append(
                            WordInfo(
                                word=word_info.word,
                                start_time=word_info.start_time.total_seconds(),
                                end_time=word_info.end_time.total_seconds(),
                            )
                        )
                    else:
                        diarized_segments.append(
                            DiarizationSpeakerTag(
                                speaker_tag=current_speaker_tag, words=current_words
                            )
                        )
                        current_speaker_tag = word_info.speaker_tag
                        current_words = [
                            WordInfo(
                                word=word_info.word,
                                start_time=word_info.start_time.total_seconds(),
                                end_time=word_info.end_time.total_seconds(),
                            )
                        ]
                if current_words:
                    diarized_segments.append(
                        DiarizationSpeakerTag(
                            speaker_tag=current_speaker_tag, words=current_words
                        )
                    )

        return TranscriptionResult(
            transcript=" ".join(full_transcript),
            word_timestamps=word_timestamps if word_timestamps else None,
            diarized_segments=diarized_segments if diarized_segments else None,
        )
    else:
        # If the operation is not done, you might want to re-poll later or raise an exception
        raise Exception("Transcription job not yet complete.")


if __name__ == "__main__":
    # Example usage (replace with a real operation name)
    # In a real scenario, you would get this operation_name from submit_transcription.py
    # operation_name = "projects/123456789/locations/us-central1/operations/your-operation-id"
    # result = poll_transcription_job(operation_name)
    # print("Full Transcript:", result.transcript)
    pass
