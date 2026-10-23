from typing import Dict, Any


def normalize_transcription_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized_response = {
        'job_id': response['TranscriptionJob']['TranscriptionJobName'],
        'status': response['TranscriptionJob']['TranscriptionJobStatus'],
    }
    if response['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        normalized_response['transcript'] = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    else:
        normalized_response['status'] = 'PENDING'
    return normalized_response


def normalize_diarization_response(response: Dict[str, Any]) -> Dict[str, Any]:
    normalized_response = {
        'job_id': response['SpeakerDiarizationJob']['SpeakerDiarizationJobName'],
        'status': response['SpeakerDiarizationJob']['SpeakerDiarizationJobStatus'],
    }
    if response['SpeakerDiarizationJob']['SpeakerDiarizationJobStatus'] == 'COMPLETED':
        normalized_response['diarization'] = response['SpeakerDiarizationJob']['SpeakerDiarizationResult']
    else:
        normalized_response['status'] = 'PENDING'
    return normalized_response