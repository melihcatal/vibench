from google.cloud import speech_v1p1beta1 as speech
from speech_client import SpeechClientWrapper
from speech_models import TranscriptionResult

def poll_transcription(job_id):
    client_wrapper = SpeechClientWrapper()
    client = client_wrapper.get_client()

    operation = client.get_operation(job_id)

    if operation.done:
        response = operation.result
        transcript_parts = []
        word_timestamps = []
        speaker_tags = []

        for result in response.results:
            transcript_parts.append(result.alternatives[0].transcript)
            for word_info in result.alternatives[0].words:
                word_timestamps.append({
                    "word": word_info.word,
                    "start_time": word_info.start_time.seconds + word_info.start_time.nanos * 1e-9,
                    "end_time": word_info.end_time.seconds + word_info.end_time.nanos * 1e-9,
                    "speaker_tag": word_info.speaker_tag if hasattr(word_info, 'speaker_tag') else None
                })
            

        return TranscriptionResult(
            job_id=job_id,
            status="COMPLETED",
            transcript=" ".join(transcript_parts),
            word_timestamps=word_timestamps,
            speaker_tags=speaker_tags if speaker_tags else None # Only include if diarization was enabled
        )
    else:
        return TranscriptionResult(
            job_id=job_id,
            status="IN_PROGRESS",
        )
