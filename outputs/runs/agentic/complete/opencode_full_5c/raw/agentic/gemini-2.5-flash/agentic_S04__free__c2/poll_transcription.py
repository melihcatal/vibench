from speech_client import get_speech_client
from speech_models import TranscriptionJob, TranscriptionResult, Alternative, WordInfo
from google.cloud import speech_v1p1beta1 as speech


def poll_transcription(operation_name: str) -> TranscriptionJob:
    client = get_speech_client()

    operation = client.transport.operations_client.get_operation(operation_name)

    if operation.done:
        response = speech.LongRunningRecognizeResponse(operation.response)
        alternatives = []
        for result in response.results:
            for alt in result.alternatives:
                words = []
                if alt.words:
                    for word_info in alt.words:
                        words.append(
                            WordInfo(
                                word=word_info.word,
                                start_time=word_info.start_time.seconds
                                + word_info.start_time.nanos / 1e9,
                                end_time=word_info.end_time.seconds
                                + word_info.end_time.nanos / 1e9,
                                speaker_tag=word_info.speaker_tag
                                if hasattr(word_info, "speaker_tag")
                                else None,
                            )
                        )
                alternatives.append(
                    Alternative(
                        transcript=alt.transcript,
                        confidence=alt.confidence,
                        words=words,
                    )
                )

        transcription_result = TranscriptionResult(
            alternatives=alternatives,
            language_code=response.results[0].language_code if response.results else "",
        )
        return TranscriptionJob(
            operation_name=operation_name,
            status="COMPLETED",
            results=transcription_result,
        )
    else:
        return TranscriptionJob(operation_name=operation_name, status="IN_PROGRESS")
