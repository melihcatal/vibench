from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError
from speech_client import get_speech_client
from speech_models import DiarizationResponse

def diarized_transcript(audio_uri: str, language_code: str = "en-US") -> DiarizationResponse:
    """
    Requests speaker diarization for a recorded meeting using Google Cloud Speech-to-Text.
    """
    client = get_speech_client()
    config = {
        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "sample_rate_hertz": 16000,
        "language_code": language_code,
        "enable_speaker_diarization": True,
        "diarization_speaker_count": 2,
        "model": "latest_long",
    }

    try:
        operation = client.long_running_recognize(
            request={
                "config": config,
                "audio": {"uri": audio_uri},
            }
        )
        operation.result()

        if operation.response:
            diarized_results = []
            for result in operation.response.results:
                for word_info in result.alternatives[0].words:
                    diarized_results.append({
                        "speaker_tag": word_info.speaker_tag,
                        "word": word_info.word,
                        "start_time": word_info.start_time.total_seconds(),
                        "end_time": word_info.end_time.total_seconds(),
                    })
            return DiarizationResponse(
                job_id=operation.operation.name,
                status="COMPLETED",
                results=diarized_results,
                error=None
            )
        else:
            return DiarizationResponse(
                job_id=None,
                status="FAILED",
                results=None,
                error="No diarization results returned"
            )
    except GoogleAPICallError as e:
        return DiarizationResponse(
            job_id=None,
            status="FAILED",
            results=None,
            error=str(e)
        )