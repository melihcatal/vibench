from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client
from speech_models import TranscriptionResult

def poll_transcription_job(operation_name: str) -> TranscriptionResult:
    client = get_speech_client()
    operation = client.long_running_recognize(request={"name": operation_name})

    print(f"Polling operation {operation_name}...")

    # This will block until the operation is complete
    response = operation.result(timeout=9000)

    transcript_builder = []
    word_timestamps = []
    diarization_speakers = []

    for result in response.results:
        # The first alternative is generally the most accurate
        alternative = result.alternatives[0]
        transcript_builder.append(alternative.transcript)

        if alternative.words:
            for word_info in alternative.words:
                word_timestamps.append({
                    "word": word_info.word,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                    "speaker_tag": word_info.speaker_tag if hasattr(word_info, 'speaker_tag') else None,
                })
        if hasattr(alternative, 'speaker_tag') and alternative.speaker_tag:
            diarization_speakers.append(alternative.speaker_tag)

    return TranscriptionResult(
        transcript=" ".join(transcript_builder),
        word_timestamps=word_timestamps if word_timestamps else None,
        diarization_speakers=list(set(diarization_speakers)) if diarization_speakers else None,
    )
