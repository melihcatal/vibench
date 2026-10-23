import requests
from speech_client import AzureSpeechClient
from speech_models import TranscriptionRequest, TranscriptionProperties, WordLevelTimestamp, ticks_to_seconds

def request_timestamped_transcript(audio_uri: str, language_code: str, job_name: str, client: AzureSpeechClient):
    properties = TranscriptionProperties(wordLevelTimestampsEnabled=True)
    request = TranscriptionRequest(
        displayName=job_name,
        locale=language_code,
        contentUrls=[audio_uri],
        properties=properties
    )
    
    response_json = client.submit_transcription(
        display_name=request.displayName,
        locale=request.locale,
        content_urls=request.contentUrls,
        properties=request.properties.__dict__ # Convert dataclass to dict for API call
    )
    return {'job_id': response_json['self'].split('/')[-1], 'status': 'SUBMITTED'}

def extract_word_timestamps(transcription_result: dict) -> list[WordLevelTimestamp]:
    timestamps = []
    for recognized_phrase in transcription_result.get('recognizedPhrases', []):
        for word_info in recognized_phrase.get('nBest', [{}])[0].get('words', []):
            timestamps.append(WordLevelTimestamp(
                word=word_info['word'],
                offset=word_info['offset'],
                duration=word_info['duration']
            ))
    return timestamps

def extract_segment_timestamps(transcription_result: dict) -> list[dict]:
    segments = []
    for recognized_phrase in transcription_result.get('recognizedPhrases', []):
        text = recognized_phrase.get('nBest', [{}])[0].get('display', '')
        offset_ticks = recognized_phrase.get('offset', 0)
        duration_ticks = recognized_phrase.get('duration', 0)
        
        segments.append({
            'text': text,
            'offset_seconds': ticks_to_seconds(offset_ticks),
            'duration_seconds': ticks_to_seconds(duration_ticks)
        })
    return segments
