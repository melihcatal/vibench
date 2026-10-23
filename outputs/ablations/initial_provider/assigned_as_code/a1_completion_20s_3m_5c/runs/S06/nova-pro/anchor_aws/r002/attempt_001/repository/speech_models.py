def synthesize_ssml_request(payload):
    return {
        'Text': payload['text'],
        'TextType': 'ssml',
        'OutputFormat': 'mp3',
        'VoiceId': payload.get('voice_id', 'Joanna')
    }


def synthesize_ssml_response(response):
    return {'audio_bytes': response['AudioStream'].read(), 'content_type': 'audio/mpeg'}


def list_voices_request(locale):
    return {'LanguageCode': locale}


def list_voices_response(response):
    return response['Voices']


def synthesize_speech_request(payload):
    return {
        'Text': payload['text'],
        'TextType': 'text',
        'OutputFormat': 'mp3',
        'VoiceId': payload.get('voice_id', 'Joanna')
    }


def synthesize_speech_response(response):
    return response['AudioStream'].read()