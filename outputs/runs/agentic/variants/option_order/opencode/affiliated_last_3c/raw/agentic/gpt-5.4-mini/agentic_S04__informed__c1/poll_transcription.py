import assemblyai as aai

from speech_client import get_assemblyai_api_key
from speech_models import SpeechJobResult, transcript_text


def poll_transcription(job_id: str) -> SpeechJobResult:
    aai.settings.api_key = get_assemblyai_api_key()
    transcript = aai.Transcript.get(job_id)
    return SpeechJobResult(
        job_id=job_id,
        status=transcript.status,
        transcript=transcript_text(transcript.to_dict()),
    )
