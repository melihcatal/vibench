from google.cloud import speech_v1 as speech

def create_transcription_request(audio_uri, config):
    return speech.types.TranscriptionConfig(audio=speech.types.Audio(uri=audio_uri), config=config)

def parse_transcription_response(response):
    results = []
    for result in response.results:
        alternatives = []
        for alternative in result.alternatives:
            alternatives.append({
                'transcript': alternative.transcript,
                'confidence': alternative.confidence
            })
        results.append({
            'alternatives': alternatives,
            'channel_tag': result.channel_tag
        })
    return results

def normalize_transcription_results(results):
    normalized_results = []
    for result in results:
        normalized_alternatives = []
        for alternative in result['alternatives']:
            normalized_alternatives.append({
                'transcript': alternative['transcript'].lower().strip(),
                'confidence': alternative['confidence']
            })
        normalized_results.append({
            'alternatives': normalized_alternatives,
            'channel_tag': result['channel_tag']
        })
    return normalized_results