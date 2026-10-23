from speech_client import speech_client
from speech_models import TranscriptionResult, WordInfo
from google.api_core.operation import Operation


def poll_transcription(operation_name: str) -> TranscriptionResult:
    operation = Operation(operation_name, speech_client.speech_client)
    response = operation.result(timeout=900000)  # 15 minutes timeout

    full_transcript = []
    words_info = []
    speaker_diarization_output = []

    for result in response.results:
        full_transcript.append(result.alternatives[0].transcript)
        for word_info in result.alternatives[0].words:
            words_info.append(
                WordInfo(
                    word=word_info.word,
                    start_time=word_info.start_time.total_seconds(),
                    end_time=word_info.end_time.total_seconds(),
                    speaker_tag=word_info.speaker_tag
                    if hasattr(word_info, "speaker_tag")
                    else None,
                )
            )
        if (
            hasattr(result.alternatives[0], "words")
            and result.alternatives[0].words
            and hasattr(result.alternatives[0].words[0], "speaker_tag")
        ):
            speaker_diarization_output.extend(
                [
                    f"Speaker {word.speaker_tag}: {word.word}"
                    for word in result.alternatives[0].words
                ]
            )

    return TranscriptionResult(
        transcript=" ".join(full_transcript),
        words=words_info if words_info else None,
        speaker_diarization=speaker_diarization_output
        if speaker_diarization_output
        else None,
    )
