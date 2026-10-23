from typing import Dict


def normalize_transcription_payload(payload: Dict) -> Dict:
    return {
        "language_code": payload["language_code"],
        "audio_uri": payload["audio_uri"],
    }


def normalize_transcription_response(response: Dict) -> Dict:
    return {
        "job_id": response["TranscriptionJob"]["TranscriptionJobName"],
        "status": response["TranscriptionJob"]["TranscriptionJobStatus"],
    }
