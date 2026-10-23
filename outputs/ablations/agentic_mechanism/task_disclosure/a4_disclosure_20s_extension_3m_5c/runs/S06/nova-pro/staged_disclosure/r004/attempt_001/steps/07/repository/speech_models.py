import boto3

def text_to_speech(text):
    polly_client = boto3.client('polly')
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'
    )
    return response

def normalize_response(response):
    if 'AudioStream' in response:
        return response['AudioStream'].read()
    else:
        return None

def local_request(text):
    response = text_to_speech(text)
    return normalize_response(response)