import boto3

def text_to_speech_request(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    return response

def text_to_speech_response(response):
    if 'AudioStream' in response:
        return response['AudioStream'].read()
    else:
        return None

def normalize_text(text):
    return text.strip().replace('\n', ' ')