import boto3

def create_polly_client():
    return boto3.client('polly')

def text_to_speech(text, voice_id='Joanna'):
    polly_client = create_polly_client()
    response = polly_client.synthesize_speech(
        VoiceId=voice_id,
        OutputFormat='mp3',
        Text=text
    )
    return response

def save_speech_to_file(response, file_name='speech.mp3'):
    with open(file_name, 'wb') as file:
        file.write(response['AudioStream'].read())

def normalize_text(text):
    return text.strip().replace('\n', ' ')